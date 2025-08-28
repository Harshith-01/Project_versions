# /backend/app/models/pydantic_models.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DiagnosisRequest(BaseModel):
    session_id: str
    free_text: str
    quantum_mode: bool
    # Store conversation history to maintain context
    symptom_history: List[Dict[str, Any]] = []

class SymptomFrame(BaseModel):
    present: List[str]
    absent: List[str]

class Diagnosis(BaseModel):
    name: str
    prob: float
    evidence: List[str]

class FollowUp(BaseModel):
    question: str
    expected_signal: str

class DiagnosisResponse(BaseModel):
    session_id: str
    final_diagnosis: bool
    diagnoses: Optional[List[Diagnosis]] = None
    follow_up_question: Optional[str] = None
    citations: Optional[List[Dict[str, str]]] = None
    red_flags: Optional[List[str]] = None
    error: Optional[str] = None