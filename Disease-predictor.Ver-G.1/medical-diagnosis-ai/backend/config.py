# /backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM & Embedding Models
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # Vector Database
    CHROMA_DIR = "./chroma"
    COLLECTION_NAME = "medical_knowledge"

    # RAG & Clarification Logic
    TOP_K = 8
    CLARIFY_THRESHOLD = 0.65
    MAX_TURNS = 3

    # Quantum-Inspired Superposition Tuning
    SUPERPOSITION_TOP_K = 3 # How many basis states to consider
    SUPERPOSITION_ALPHA = 0.6 # Weight of original query vs. retrieved states