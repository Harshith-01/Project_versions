import json
from .config import COLUMNS, GENDER_VALUES, AGE_GROUP_VALUES, SEVERITY_VALUES, GEMINI_API_KEY, MODEL_NAME
from .mapping import to_canonical
from .llm import Row, ExtractResult, clamp, postprocess, fallback_extract

import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def extract_rows(disease: str, source_text: str, source_url: str, model_version: str) -> ExtractResult:
    """
    Use Gemini to extract structured probabilistic rows from raw text.
    Falls back to heuristic extractor if LLM fails.
    """
    try:
        prompt = f"""
You are a medical dataset builder.
Task: extract multiple *realistic* patient presentation rows for the disease: {disease}.
Source text (trusted medical site):
---
{source_text[:15000]}
---

Rules:
- Output ONLY valid JSON matching this schema:
{{
  "rows": [
    {{
      "disease": "{disease}",
      "symptom_summary": "short free-text summary",
      "gender": "male|female|other|all",
      "age_group": "child|adolescent|adult|elderly|all",
      "severity_level": "mild|moderate|severe|critical|unspecified",
      "duration_days": number or null,
      "features": {{
        "fever": float, "fatigue": float, ..., "mood_swings": float
      }}
    }},
    ...
  ]
}}
- Each feature is a probability between 0.0–1.0.
- Provide 2–6 rows capturing common variations (e.g. mild, severe, child, elderly).
- Do not include explanations, only JSON.
        """

        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.4}
        )

        raw_text = response.text.strip()
        data = json.loads(raw_text)   # parse Gemini JSON
        return postprocess(data, source_url, model_version)

    except Exception as e:
        print("LLM call failed, falling back to keyword extractor:", e)
        return fallback_extract(disease, source_text, source_url, model_version)
