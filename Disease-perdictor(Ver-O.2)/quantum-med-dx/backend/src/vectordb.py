import chromadb
from chromadb.config import Settings
from config import settings

_client = None
_collection = None
NAME = "medical_chunks"

def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.Client(Settings(persist_directory=settings.CHROMA_DIR))
        _collection = _client.get_or_create_collection(NAME, metadata={"hnsw:space":"cosine"})
    return _collection

def upsert_chunks(chunks):
    col = get_collection()
    col.upsert(
        ids=[c["id"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{k:v for k,v in c.items() if k not in ("id","text","embedding")} for c in chunks]
    )

def query_similar(query_embedding, top_k=8):
    col = get_collection()
    res = col.query(query_embeddings=[query_embedding], n_results=top_k)
    out = []
    for i in range(len(res["ids"][0])):
        out.append({
            "id": res["ids"][0][i],
            "text": res["documents"][0][i],
            "source_url": res["metadatas"][0][i].get("source_url",""),
            "disease": res["metadatas"][0][i].get("disease"),
            "section": res["metadatas"][0][i].get("section"),
        })
    return out
