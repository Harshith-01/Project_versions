from flask import Blueprint, request, jsonify
from ..schemas import IngestItem
from ..ingest import ingest_urls

ingest_bp = Blueprint("ingest", __name__)

@ingest_bp.post("/ingest")
def ingest():
    data = request.get_json(force=True)
    items = [IngestItem(**d).model_dump() for d in data.get("items",[])]
    res = ingest_urls(items)
    return jsonify(res)
