from .embeddings import embed_text
from .vectordb import query_similar

def retrieve(frame: dict, top_k: int):
    from .utils import frame_to_query
    q = frame_to_query(frame)
    e = embed_text(q)
    docs = query_similar(e, top_k=top_k)
    # attach ctx_id
    for i, d in enumerate(docs):
        d["ctx_id"] = f"ctx#{i}"
    return docs
