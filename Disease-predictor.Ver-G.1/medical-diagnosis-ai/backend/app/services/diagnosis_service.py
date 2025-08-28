# /backend/app/services/diagnosis_service.py
import numpy as np
from .retrieval_service import RetrievalService
from .llm_service import LLMService
from .quantum_service import QuantumService
from config import Config
import re

class DiagnosisService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()
        self.quantum_service = QuantumService()

    def _parse_symptoms(self, text: str, history: list) -> dict:
        """Parses free text for symptoms, handles simple negations, and combines with history."""
        # This function remains the same as before
        negation_patterns = r"\b(no|without|not|denies|denied|never had a)\b\s*([a-zA-Z\s,]+)"
        negations = re.findall(negation_patterns, text, re.IGNORECASE)
        absent_symptoms = [symptom.strip().lower() for _, symptom in negations]
        positive_text = re.sub(negation_patterns, "", text, flags=re.IGNORECASE)
        present_symptoms = [word.strip().lower() for word in re.split(r'[\s,and]+', positive_text) if len(word) > 2]
        combined_present = set(s for item in history if item['type'] == 'present' for s in item['symptoms'])
        combined_absent = set(s for item in history if item['type'] == 'absent' for s in item['symptoms'])
        combined_present.update(s for s in present_symptoms if s not in absent_symptoms)
        combined_absent.update(absent_symptoms)
        return {"present": list(combined_present), "absent": list(combined_absent)}

    def _create_superposition_query(self, query_text: str) -> str:
        """
        Quantum-Inspired Enhancement: Creates a superposition of the user's ambiguous state
        by blending the initial query with the most likely diagnostic states.
        """
        print("Creating symptom superposition query...")
        # 1. Initial Retrieval to find "basis states"
        initial_results = self.retrieval_service.search(
            query_text,
            top_k=Config.SUPERPOSITION_TOP_K,
            include_embeddings=True
        )

        original_embedding = self.retrieval_service.embed_text(query_text)
        retrieved_embeddings = np.array(initial_results['embeddings'][0])

        if retrieved_embeddings.size == 0:
            return original_embedding # Fallback

        # 2. Blend embeddings to create the superposition state
        # Weighted average of the original query and the retrieved document embeddings
        avg_retrieved_embedding = np.mean(retrieved_embeddings, axis=0)
        
        alpha = Config.SUPERPOSITION_ALPHA
        superposition_embedding = (alpha * original_embedding) + ((1 - alpha) * avg_retrieved_embedding)
        
        return superposition_embedding.tolist()


    def process_request(self, request_data):
        session_id = request_data.session_id
        current_turn = len(request_data.symptom_history) // 2
        
        symptom_frame = self._parse_symptoms(request_data.free_text, request_data.symptom_history)
        if not symptom_frame["present"]:
            return {"session_id": session_id, "final_diagnosis": True, "error": "Please describe your symptoms."}

        # 2. Build query text
        query_text = f"Symptoms present: {', '.join(symptom_frame['present'])}. Symptoms absent: {', '.join(symptom_frame['absent'])}."
        
        # 3. QUANTUM-INSPIRED: Create and use the superposition query
        superposition_query_embedding = self._create_superposition_query(query_text)

        # 4. Final Retrieval (the "Measurement")
        print("Performing final retrieval (measurement) on superposition state...")
        retrieved = self.retrieval_service.search(
            query_embedding=superposition_query_embedding, 
            top_k=Config.TOP_K
        )
        context_docs = retrieved.get('documents', [[]])[0]
        context_metadatas = retrieved.get('metadatas', [[]])[0]

        # 5. Call LLM for reasoning (leveraging "Conceptual Entanglement" in the prompt)
        llm_output = self.llm_service.generate_response(symptom_frame, context_docs)

        if "error" in llm_output:
            return {"session_id": session_id, "final_diagnosis": True, "error": llm_output["error"]}
        
        diagnoses = llm_output.get("differential_diagnoses", [])
        citations = self._create_citations(llm_output, context_metadatas)

        # 6. Clarification Logic (with direct Quantum option)
        max_prob = max([d.get('prob', 0) for d in diagnoses]) if diagnoses else 0
        if max_prob < Config.CLARIFY_THRESHOLD and current_turn < Config.MAX_TURNS:
            follow_up_question = self._select_followup(llm_output.get("candidate_followups", []), request_data.quantum_mode)
            if follow_up_question:
                return {"session_id": session_id, "final_diagnosis": False, "diagnoses": diagnoses, "follow_up_question": follow_up_question, "citations": citations, "red_flags": llm_output.get("red_flags")}

        # 7. Finalize and return
        return {"session_id": session_id, "final_diagnosis": True, "diagnoses": diagnoses, "citations": citations, "red_flags": llm_output.get("red_flags")}

    def _select_followup(self, candidates: list, use_quantum: bool) -> str:
        if not candidates: return None
        weights = [1.0] * len(candidates) # Simple heuristic
        if use_quantum:
            print("Using Qiskit for follow-up question...")
            chosen_index = self.quantum_service.sample_question(weights)
        else:
            print("Using classical sampling for follow-up question...")
            probabilities = np.array(weights) / np.sum(weights)
            chosen_index = np.random.choice(len(candidates), p=probabilities)
        return candidates[chosen_index]['question']

    def _create_citations(self, llm_output, metadatas):
        # This function remains the same as before
        evidence_ids = {ev for diag in llm_output.get("differential_diagnoses", []) for ev in diag.get("evidence", [])}
        citations = []
        for ev_id in sorted(list(evidence_ids)):
            try:
                idx = int(ev_id.split('_')[1]) - 1
                if 0 <= idx < len(metadatas):
                    meta = metadatas[idx]
                    citations.append({"id": ev_id, "source": meta.get("source_url", "N/A"), "disease": meta.get("disease", "N/A")})
            except (ValueError, IndexError):
                continue
        return citations