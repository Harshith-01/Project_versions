# /backend/app/services/ingestion_service.py
import chromadb
from sentence_transformers import SentenceTransformer
from config import Config

class IngestionService:
    def __init__(self):
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.chroma_client = chromadb.PersistentClient(path=Config.CHROMA_DIR)
        self.collection = self.chroma_client.get_or_create_collection(
            name=Config.COLLECTION_NAME
        )

    def ingest_from_json(self, data):
        """
        Processes and ingests data from a JSON object.
        Data is expected to be a list of dicts, each with 'disease', 'url', and 'content'.
        """
        documents = []
        metadatas = []
        ids = []
        doc_id = 1

        for item in data:
            disease = item.get("disease", "Unknown")
            url = item.get("url", "")
            content = item.get("content", {})

            for section, text in content.items():
                if not text:
                    continue
                documents.append(text)
                metadatas.append({
                    "disease": disease,
                    "section": section,
                    "source_url": url
                })
                ids.append(f"doc_{doc_id}")
                doc_id += 1
        
        if not documents:
            print("No documents to ingest.")
            return

        print(f"Ingesting {len(documents)} document chunks...")
        # Embed and upsert in batches if necessary, but for small data this is fine
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Ingestion complete.")