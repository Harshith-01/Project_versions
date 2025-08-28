from flask import Flask, request, jsonify
from flask import make_response
from schemas import DiagnoseRequest, FollowupRequest
from config import Config
from rag import similarity_search
from llm import call_llm
from utils import extract_negations, frame_to_query, softmax, choose_classical, generate_id
from quantum import quantum_sample
import json
import os

app = Flask(__name__)

def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = Config.ALLOWED_ORIGINS
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return resp

@app.after_request
def add_cors(resp):
    return cors(resp)

@app.route("/health", methods=["GET", "OPTIONS"])
def health():
    return cors(make_response({"status":"ok"}))

SESSION_LOGS = {}  # in-memory; swap to DB for prod

@app.route("/diagnose", methods=["POST", "OPTIONS"])
def diagnose():
    if request.method == "OPTIONS":
        return cors(make_response(("", 204)))
    payload = request.get_json(force=True)
    dreq = DiagnoseRequest(**payload)

    quantum_mode = Config.QUANTUM_FOLLOWUPS_DEFAULT if dreq.quantum_mode is None else dreq.quantum_mode

    # Build symptom frame (basic: present/absent from negation extraction)
    neg = extract_negations(dreq.free_text)
    present = sorted(set(neg["present"] + dreq.checkbox_symptoms))
    absent = sorted(set(neg["absent"]))
    symptom_frame = {
        "present": present,
        "absent": absent,
        "duration_days": None
    }

    # Retrieval
    q = frame_to_query(symptom_frame)
    context = similarity_search(q, k=Config.TOP_K)

    # LLM call
    llm_out = call_llm(symptom_frame, context)

    # Confidence check
    diffs = llm_out.get("differential_diagnoses", [])
    probs = [float(x.get("prob", 0.0)) for x in diffs] or [0.0]
    top_prob = max(probs)
    ask_followup = None
    chosen_idx = None
    candidate_followups = llm_out.get("candidate_followups", [])

    trace_id = generate_id()
    SESSION_LOGS.setdefault(dreq.session_id, {"turns": 0, "traces": []})

    if top_prob < Config.CLARIFY_THRESHOLD and candidate_followups:
        # Heuristic weights: prefer rule-in for top diseases
        weights = [1.0 for _ in candidate_followups]
        weights = softmax(weights)

        if quantum_mode:
            chosen_idx = quantum_sample(weights)
        else:
            chosen_idx = choose_classical(weights)

        chosen_idx = min(max(0, chosen_idx), len(candidate_followups)-1)
        ask_followup = candidate_followups[chosen_idx]["question"]

        SESSION_LOGS[dreq.session_id]["traces"].append({
            "trace_id": trace_id,
            "symptom_frame": symptom_frame,
            "context_ids": [c["ctx_id"] for c in context],
            "llm_out": llm_out,
            "quantum_mode": quantum_mode,
            "followup_question": ask_followup
        })

        return cors(make_response(jsonify({
            "status": "clarify",
            "trace_id": trace_id,
            "question": ask_followup,
            "citations": [{"ctx_id": c["ctx_id"], "url": c["source_url"], "section": c["section"]} for c in context],
            "note": "Confidence below threshold; asking a clarifying question.",
            "quantum_mode": quantum_mode,
            "disclaimer": "This system is not a medical device. Consult a clinician."
        })))

    # Finalize
    SESSION_LOGS[dreq.session_id]["traces"].append({
        "trace_id": trace_id,
        "symptom_frame": symptom_frame,
        "context_ids": [c["ctx_id"] for c in context],
        "llm_out": llm_out,
        "quantum_mode": quantum_mode,
        "followup_question": None
    })

    top = sorted(diffs, key=lambda x: x.get("prob",0.0), reverse=True)[:3]
    return cors(make_response(jsonify({
        "status": "final",
        "trace_id": trace_id,
        "top_diagnoses": top,
        "recommended_tests": llm_out.get("recommended_tests", []),
        "red_flags": llm_out.get("red_flags", []),
        "citations": [{"ctx_id": c["ctx_id"], "url": c["source_url"], "section": c["section"]} for c in context],
        "quantum_mode": quantum_mode,
        "disclaimer": "This system is not a medical device. Consult a clinician."
    })))

@app.route("/clarify", methods=["POST", "OPTIONS"])
def clarify():
    if request.method == "OPTIONS":
        return cors(make_response(("", 204)))
    payload = request.get_json(force=True)
    freq = FollowupRequest(**payload)
    session = SESSION_LOGS.get(freq.session_id)
    if not session or not session["traces"]:
        return cors(make_response(jsonify({"error":"session not found"}), 404))

    # take last trace and enrich the frame with the answer
    last = session["traces"][-1]
    frame = dict(last["symptom_frame"])
    q = freq.chosen_question.lower()
    # naive mapping: add to present/absent based on yes/no
    token = q.split("?")[0].strip().split()[-1] if q else "symptom"
    if freq.answer == "yes":
        frame["present"] = sorted(set(frame.get("present", []) + [token]))
    elif freq.answer == "no":
        frame["absent"] = sorted(set(frame.get("absent", []) + [token]))

    # Retrieval with updated frame
    query = frame_to_query(frame)
    context = similarity_search(query, k=Config.TOP_K)
    llm_out = call_llm(frame, context)

    diffs = llm_out.get("differential_diagnoses", [])
    top = sorted(diffs, key=lambda x: x.get("prob",0.0), reverse=True)[:3]

    session["traces"].append({
        "trace_id": last["trace_id"],
        "updated": True,
        "followup_answer": freq.answer,
        "symptom_frame": frame,
        "context_ids": [c["ctx_id"] for c in context],
        "llm_out": llm_out,
        "quantum_mode": bool(freq.quantum_mode)
    })

    return cors(make_response(jsonify({
        "status": "final",
        "trace_id": last["trace_id"],
        "top_diagnoses": top,
        "recommended_tests": llm_out.get("recommended_tests", []),
        "red_flags": llm_out.get("red_flags", []),
        "citations": [{"ctx_id": c["ctx_id"], "url": c["source_url"], "section": c["section"]} for c in context],
        "quantum_mode": bool(freq.quantum_mode),
        "disclaimer": "This system is not a medical device. Consult a clinician."
    })))

if __name__ == "__main__":
    # Simple run:  flask --app app run --port 8000
    app.run(host="0.0.0.0", port=8000, debug=True)
