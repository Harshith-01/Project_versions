import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER","gemini").lower()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")

    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
    CHROMA_DIR = os.getenv("CHROMA_DIR","./data/chroma")
    TOP_K = int(os.getenv("TOP_K","8"))
    CLARIFY_THRESHOLD = float(os.getenv("CLARIFY_THRESHOLD","0.65"))
    MAX_TURNS = int(os.getenv("MAX_TURNS","2"))
    QUANTUM_FOLLOWUPS = os.getenv("QUANTUM_FOLLOWUPS","true").lower() == "true"
    ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN","*")

settings = Settings()
