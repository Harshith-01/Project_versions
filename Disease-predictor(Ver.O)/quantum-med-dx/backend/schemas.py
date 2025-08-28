from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DiagnoseRequest(BaseModel):
    session_id: str
    free_text: str = ""
    checkbox_symptoms: List[str] = []
    quantum_mode: Optional[bool] = None

class FollowupRequest(BaseModel):
    session_id: str
    answer: str  # "yes" | "no" | "unsure"
    chosen_question: str
    quantum_mode: Optional[bool] = None
    previous_trace_id: Optional[str] = None

class Chunk(BaseModel):
    id: str
    text: str
    source_url: str
    disease: Optional[str] = None
    section: Optional[str] = None
    last_reviewed: Optional[str] = None

class LLMOutput(BaseModel):
    differential_diagnoses: List[Dict[str, Any]]
    candidate_followups: List[Dict[str, str]]
    recommended_tests: List[str]
    red_flags: List[str]

class FinalResponse(BaseModel):
    top_diagnoses: List[Dict[str, Any]]
    explanations: List[Dict[str, Any]]
    next_steps: List[str]
    sources: List[Dict[str, str]]
    quantum_mode: bool
    turns: int
    disclaimer: str = "This system is not a medical device. Consult a licensed clinician for diagnosis or treatment."
