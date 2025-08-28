import json
from typing import List, Dict, Any
from config import Config

# Gemini
import google.generativeai as genai
# OpenAI (optional swap)
from openai import OpenAI

def _ensure_clients():
    if Config.MODEL_PROVIDER == "gemini":
        if not Config.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY not set")
        genai.configure(api_key=Config.GEMINI_API_KEY)
    elif Config.MODEL_PROVIDER == "openai":
        if not Config.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set")

def call_llm(symptom_frame: Dict[str, Any], context_chunks: List[Dict[str,Any]]) -> Dict[str, Any]:
    """
    Returns structured JSON with differential_diagnoses, candidate_followups, recommended_tests, red_flags.
    """
    _ensure_clients()

    schema_instruction = """
Return STRICT JSON with keys:
- differential_diagnoses: list of {name: str, prob: float in [0,1], evidence: list of ctx_id strings}
- candidate_followups: list of {question: str, expected_signal: "rule_in"|"rule_out"}
- recommended_tests: list of strings
- red_flags: list of strings
Only use evidence from provided context and cite ctx_id like "ctx#1".
If insufficient context, ask for clarifying symptom questions.
"""

    ctx_text = []
    for c in context_chunks:
        header = f"[{c['ctx_id']}] ({c.get('section','unknown')}) {c.get('disease','')} <{c.get('source_url','')}>"
        body = c['text'][:1200]
        ctx_text.append(header + "\n" + body)
    ctx_join = "\n\n---\n\n".join(ctx_text)

    user_payload = {
        "symptom_frame": symptom_frame,
        "context": ctx_join
    }

    if Config.MODEL_PROVIDER == "gemini":
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"You are a medical triage assistant. Use ONLY the provided context. Cite ctx_id. {schema_instruction}\n\nUSER:\n{json.dumps(user_payload)}"
        resp = model.generate_content(prompt)
        text = resp.text or "{}"
    else:
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        content = f"You are a medical triage assistant. Use ONLY the provided context. Cite ctx_id. {schema_instruction}\n\nUSER:\n{json.dumps(user_payload)}"
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":content}],
            temperature=0.2
        )
        text = resp.choices[0].message.content

    # Best-effort JSON extraction
    start = text.find("{")
    end = text.rfind("}")
    if start >=0 and end > start:
        text = text[start:end+1]
    try:
        data = json.loads(text)
    except Exception:
        data = {
            "differential_diagnoses": [],
            "candidate_followups": [{"question":"Can you describe additional symptoms?","expected_signal":"rule_in"}],
            "recommended_tests": [],
            "red_flags": []
        }
    # Normalize probs
    diffs = data.get("differential_diagnoses", [])
    s = sum([max(0.0, float(x.get("prob", 0.0))) for x in diffs]) or 1.0
    for x in diffs:
        x["prob"] = max(0.0, float(x.get("prob", 0.0))) / s
        x["evidence"] = x.get("evidence", [])
    return data
