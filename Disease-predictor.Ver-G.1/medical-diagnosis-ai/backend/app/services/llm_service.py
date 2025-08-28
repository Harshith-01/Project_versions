# /backend/app/services/llm_service.py
import google.generativeai as genai
import json
from config import Config

class LLMService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, symptom_frame: dict, context_chunks: list) -> dict:
        # This prompt structure forces the LLM's attention mechanism to create
        # strong contextual links (conceptual entanglement) between symptoms and their status.
        system_prompt = """
        You are an expert medical triage assistant. Your role is to analyze user-provided symptoms and knowledge base context to form a differential diagnosis.
        RULES:
        1. Base your analysis ONLY on the provided context chunks. Do not use outside knowledge.
        2. Cite evidence using context chunk IDs (e.g., "ctx_1").
        3. Provide probabilities as floats between 0.0 and 1.0, summing close to 1.0.
        4. If context is insufficient, generate relevant clarifying yes/no questions.
        5. Identify any "Red Flags" from the context that match the user's symptoms.
        6. Output a single, valid JSON object with no extra text.
        """

        context_str = "\n\n".join([f"ID: ctx_{i+1}\nContent: {chunk}" for i, chunk in enumerate(context_chunks)])

        output_schema = {
            "differential_diagnoses": [{"name": "string", "prob": 0.0, "evidence": ["ctx_..."]}],
            "candidate_followups": [{"question": "string", "expected_signal": "rule_in or rule_out"}],
            "recommended_tests": ["string"],
            "red_flags": ["string"]
        }

        user_prompt = f"""
        **Knowledge Base Context:**
        {context_str}

        **Patient Symptom Frame:**
        // This structured format helps the model "entangle" symptoms with their presence or absence.
        {json.dumps(symptom_frame, indent=2)}

        **Task:**
        Analyze the symptoms and context, then generate a response strictly following this JSON schema:
        {json.dumps(output_schema, indent=2)}
        """

        try:
            response = self.model.generate_content([system_prompt, user_prompt])
            json_text = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(json_text)
        except Exception as e:
            print(f"LLM Error: {e}\nResponse Text: {response.text}")
            return {"error": "Failed to get a valid response from the LLM.", "details": str(e)}