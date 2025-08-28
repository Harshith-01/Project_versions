SYSTEM_INSTRUCTIONS = (
"You are a cautious medical triage assistant. Use ONLY the provided context. "
"Cite evidence by ctx_id (e.g., 'ctx#3'). Never invent facts. Always add a short disclaimer."
)

OUTPUT_JSON_SCHEMA = """
Return a JSON object with keys:
- differential_diagnoses: array of {name, prob (0..1), evidence: [ctx#ids]}
- candidate_followups: array of {question, expected_signal: rule_in|rule_out|clarify}
- recommended_tests: array of strings
- red_flags: array of strings
"""

def build_user_prompt(symptom_frame: dict, chunks: list[dict]) -> str:
    ctx_lines = []
    for i, ch in enumerate(chunks):
        ctx_lines.append(f"[ctx#{i}] ({ch.get('section','')}) {ch['text'][:800]}\nsource: {ch['source_url']}")
    ctx_block = "\n\n".join(ctx_lines)
    return (
        f"SYMPTOM_FRAME:\n{symptom_frame}\n\n"
        f"CONTEXT CHUNKS (authoritative medical sources):\n{ctx_block}\n\n"
        f"{OUTPUT_JSON_SCHEMA}\n"
        f"Respond with STRICT JSON only."
    )
