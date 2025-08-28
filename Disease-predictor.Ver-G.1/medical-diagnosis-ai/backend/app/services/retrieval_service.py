# /backend/app/services/retrieval_service.py
import chromadb
from sentence_transformers import SentenceTransformer
from config import Config

class RetrievalService:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RetrievalService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized: return
        print("Initializing RetrievalService...")
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.chroma_client = chromadb.PersistentClient(path=Config.CHROMA_DIR)
        self.collection = self.chroma_client.get_or_create_collection(name=Config.COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
        self._initialized = True
    
    def embed_text(self, text: str):
        return self.embedding_model.encode(text)

    def search(self, query_text: str = None, query_embedding = None, top_k: int = Config.TOP_K, include_embeddings: bool = False):
        if query_embedding is None and query_text is not None:
            query_embedding = self.embed_text(query_text).tolist()
        elif query_embedding is not None:
            # Already a list
            pass
        else:
            raise ValueError("Either query_text or query_embedding must be provided.")
        
        include_fields = ["documents", "metadatas"]
        if include_embeddings:
            include_fields.append("embeddings")

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=include_fields
        )
        return results