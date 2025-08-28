import hashlib, re
from bs4 import BeautifulSoup
import requests
from .embeddings import embed_text
from .vectordb import upsert_chunks

def fetch_clean(url: str) -> str:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    # remove nav/footers
    for tag in soup(["script","style","nav","footer","header"]): tag.decompose()
    text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    return text

def chunk(text: str, size=900, overlap=150):
    words = text.split()
    i = 0
    while i < len(words):
        part = " ".join(words[i:i+size])
        yield part
        i += (size - overlap)

def detect_section(block: str):
    s = block.lower()
    if "symptom" in s: return "Symptoms"
    if "diagnos" in s: return "Diagnosis"
    if "red flag" in s or "seek" in s and "immediate" in s: return "Red-flags"
    return "Overview"

def ingest_urls(urls: list[dict]):
    docs = []
    for item in urls:
        url = item["url"]
        disease = item.get("disease")
        text = fetch_clean(url)
        for i, part in enumerate(chunk(text)):
            sec = detect_section(part)
            _id = hashlib.md5(f"{url}::{i}".encode()).hexdigest()
            docs.append({
                "id": _id,
                "text": part,
                "embedding": embed_text(part),
                "source_url": url,
                "disease": disease,
                "section": sec,
            })
    upsert_chunks(docs)
    return {"ingested": len(docs)}
