from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class IngestItem(BaseModel):
    url: str
    disease: Optional[str] = None
    section: Optional[Literal["Symptoms","Diagnosis","Red-flags","Overview","Treatment"]] = None

class DiagnoseRequest(BaseModel):
    free_text: str
    checkboxes: Optional[List[str]] = None
    quantum_mode: bool = True
    session_id: Optional[str] = None

class RetrievedChunk(BaseModel):
    id: str
    text: str
    source_url: str
    disease: Optional[str] = None
    section: Optional[str] = None
    ctx_id: str

class DifferentialItem(BaseModel):
    name: str
    prob: float
    evidence: List[str] = []

class FollowupCandidate(BaseModel):
    question: str
    expected_signal: Literal["rule_in","rule_out","clarify"]

class LLMResult(BaseModel):
    differential_diagnoses: List[DifferentialItem] = []
    candidate_followups: List[FollowupCandidate] = []
    recommended_tests: List[str] = []
    red_flags: List[str] = []

class DiagnoseResponse(BaseModel):
    ask_followup: Optional[str] = None
    final: Optional[Dict[str, Any]] = None
    citations: List[Dict[str,str]] = []
    clarifier_mode: Literal["classical","quantum","skipped"]
