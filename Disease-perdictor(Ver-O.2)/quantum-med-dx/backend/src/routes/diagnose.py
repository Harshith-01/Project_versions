from flask import Blueprint, request, jsonify
from ..schemas import DiagnoseRequest, DiagnoseResponse
from ..negation import parse_symptoms
from ..retriever import retrieve
from ..llm_client import call_llm
from ..utils import normalize_probs
from ..clarifier import pick_followup
from config import settings

diagnose_bp = Blueprint("diagnose", __name__)

@diagnose_bp.post("/diagnose")
def diagnose():
    body = DiagnoseRequest(**request.get_json(force=True))
    frame = parse_symptoms(body.free_text, body.checkboxes or [])
    chunks = retrieve(frame, settings.TOP_K)

    llm_out = call_llm(frame, chunks)
    diffs = normalize_probs([d for d in llm_out.get("differential_diagnoses", [])])

    max_prob = max([d["prob"] for d in diffs], default=0.0)
    citations = [{"ctx_id": f"ctx#{i}", "url": c["source_url"]} for i, c in enumerate(chunks)]

    if max_prob < settings.CLARIFY_THRESHOLD and llm_out.get("candidate_followups"):
        q, mode = pick_followup(llm_out["candidate_followups"], diffs, body.quantum_mode)
        if q:
            resp = DiagnoseResponse(
                ask_followup=q,
                final=None,
                citations=citations,
                clarifier_mode=mode
            )
            return jsonify(resp.model_dump())

    # finalize
    final = {
        "differential_diagnoses": diffs,
        "recommended_tests": llm_out.get("recommended_tests", []),
        "red_flags": llm_out.get("red_flags", []),
        "disclaimer": "This is not medical advice. If symptoms worsen or red flags are present, seek urgent care."
    }
    resp = DiagnoseResponse(ask_followup=None, final=final, citations=citations, clarifier_mode="skipped")
    return jsonify(resp.model_dump())
