from sentence_transformers import SentenceTransformer
from config import settings

_model = None

def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model

def embed_text(text: str):
    model = get_embedder()
    return model.encode([text], normalize_embeddings=True)[0].tolist()
