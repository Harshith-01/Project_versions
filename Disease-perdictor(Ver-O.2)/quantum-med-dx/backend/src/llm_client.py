import json
from config import settings
from .prompts import SYSTEM_INSTRUCTIONS, build_user_prompt

# Gemini
def _gemini_call(symptom_frame, chunks):
    import google.generativeai as genai
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = build_user_prompt(symptom_frame, chunks)
    res = model.generate_content([SYSTEM_INSTRUCTIONS, prompt])
    text = res.text.strip()
    # ensure JSON only
    try:
        return json.loads(text)
    except Exception:
        # attempt to extract last JSON block
        s = text.find("{")
        e = text.rfind("}")
        return json.loads(text[s:e+1])

# OpenAI (optional)
def _openai_call(symptom_frame, chunks):
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = build_user_prompt(symptom_frame, chunks)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":SYSTEM_INSTRUCTIONS},
                  {"role":"user","content":prompt}],
        response_format={"type":"json_object"},
        temperature=0.2,
    )
    return json.loads(resp.choices[0].message.content)

def call_llm(symptom_frame, chunks):
    if settings.MODEL_PROVIDER == "openai":
        return _openai_call(symptom_frame, chunks)
    return _gemini_call(symptom_frame, chunks)
