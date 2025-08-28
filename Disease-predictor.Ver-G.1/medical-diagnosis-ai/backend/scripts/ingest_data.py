# /backend/scripts/ingest_data.py
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.ingestion_service import IngestionService

def main():
    print("Starting data ingestion...")
    ingestion_service = IngestionService()
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base.json')
    try:
        with open(file_path, 'r') as f:
            knowledge_data = json.load(f)
    except Exception as e:
        print(f"Error reading knowledge base file: {e}")
        return
    ingestion_service.ingest_from_json(knowledge_data)
    print("Data ingestion completed successfully.")

if __name__ == "__main__":
    main()