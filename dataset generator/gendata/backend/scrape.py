import httpx
from readability import Document
import trafilatura
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DatasetBuilder/1.0)"}

async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient(timeout=30.0, headers=HEADERS, follow_redirects=True) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text

async def extract_text(url: str) -> str:
    """
    Try trafilatura extraction first; fallback to readability + BeautifulSoup cleanup.
    Returns cleaned plain text.
    """
    html = await fetch_html(url)
    text = trafilatura.extract(html, include_tables=False, include_links=False)
    if text:
        return text
    doc = Document(html)
    cleaned_html = doc.summary()
    soup = BeautifulSoup(cleaned_html, "lxml")
    for tag in soup(["script","style","nav","footer","header","aside"]):
        tag.decompose()
    text = soup.get_text(" ")
    return " ".join(text.split())
