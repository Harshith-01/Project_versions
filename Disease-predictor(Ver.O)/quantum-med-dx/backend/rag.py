import os
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

from config import Config

EMB_MODEL = None
VECTORSTORE = None

def init_embeddings():
    global EMB_MODEL
    if EMB_MODEL is None:
        EMB_MODEL = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)

def get_vectorstore(persist_dir: str = None):
    global VECTORSTORE
    if VECTORSTORE is None:
        init_embeddings()
        persist_dir = persist_dir or Config.CHROMA_DIR
        VECTORSTORE = Chroma(
            embedding_function=EMB_MODEL,
            persist_directory=persist_dir,
            collection_name="medical_docs"
        )
    return VECTORSTORE

def upsert_docs(docs: List[Dict[str, Any]]):
    """
    docs: [{text, metadata: {source_url, disease, section, last_reviewed}}]
    """
    vs = get_vectorstore()
    lang_docs = [Document(page_content=d["text"], metadata=d.get("metadata", {})) for d in docs]
    vs.add_documents(lang_docs)
    vs.persist()

def similarity_search(query: str, k: int) -> List[Dict[str, Any]]:
    vs = get_vectorstore()
    results = vs.similarity_search_with_score(query, k=k)
    ctx = []
    for doc, score in results:
        meta = doc.metadata or {}
        ctx.append({
            "ctx_id": f"ctx#{len(ctx)+1}",
            "text": doc.page_content,
            "score": float(score),
            "source_url": meta.get("source_url",""),
            "disease": meta.get("disease"),
            "section": meta.get("section"),
            "last_reviewed": meta.get("last_reviewed")
        })
    return ctx
