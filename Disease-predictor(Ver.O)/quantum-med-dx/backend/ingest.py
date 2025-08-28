"""
Ingest trusted URLs -> clean -> chunk -> embed -> upsert to Chroma.
Run:
  uv run python ingest.py
or
  python ingest.py
"""
import os, re, time, yaml, requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
from rag import upsert_docs
from config import Config

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SOURCES_YAML = os.path.join(DATA_DIR, "sources.yaml")

def fetch_clean(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    # Basic cleaner
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text(text: str, size=1200, overlap=200) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+size])
        chunks.append(chunk)
        i += (size - overlap)
    return chunks

def detect_section(chunk: str) -> str:
    low = chunk.lower()
    if "symptom" in low: return "Symptoms"
    if "diagnos" in low: return "Diagnosis"
    if "treatment" in low: return "Treatment"
    if "risk" in low: return "Risk factors"
    if "prevention" in low: return "Prevention"
    if "warning" in low or "urgent" in low or "red flag" in low: return "Red-flags"
    return "General"

def run():
    with open(SOURCES_YAML, "r") as f:
        sources = yaml.safe_load(f)

    docs = []
    now = datetime.utcnow().date().isoformat()
    for item in sources.get("sources", []):
        url = item["url"]
        disease = item.get("disease")
        print(f"[ingest] fetching {url}")
        try:
            text = fetch_clean(url)
        except Exception as e:
            print(f"[ingest] failed {url}: {e}")
            continue
        for ch in chunk_text(text):
            meta = {
                "source_url": url,
                "disease": disease,
                "section": detect_section(ch),
                "last_reviewed": now
            }
            docs.append({"text": ch, "metadata": meta})

    print(f"[ingest] upserting {len(docs)} chunks ...")
    upsert_docs(docs)
    print("[ingest] done.")

if __name__ == "__main__":
    run()
