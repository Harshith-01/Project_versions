from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import io, os, datetime
from .config import DATASET_CSV, COLUMNS, PORT, MODEL_NAME
from .scrape import extract_text
from .llm import extract_rows
from .utils import ensure_csv_exists, append_rows

app = FastAPI(title="Disease Dataset Builder API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

ensure_csv_exists()

class IngestRequest(BaseModel):
    url: str
    disease: str

@app.post("/ingest-url")
async def ingest_url(req: IngestRequest):
    # fetch + extract text from URL
    text = await extract_text(req.url)
    result = extract_rows(req.disease, text, source_url=req.url, model_version=MODEL_NAME)

    rows = []
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    for r in result.rows:
        row = {c: None for c in COLUMNS}
        row.update({
            "disease": r.disease or req.disease,
            "symptom_summary": r.symptom_summary,
            "gender": r.gender,
            "age_group": r.age_group,
            "severity_level": r.severity_level,
            "duration_days": r.duration_days,
            "source_url": req.url,
            "retrieved_at": ts,
            "model_version": MODEL_NAME
        })
        for k, v in r.features.items():
            row[k] = v
        rows.append(row)

    df_new = pd.DataFrame(rows, columns=COLUMNS)
    added, total = append_rows(df_new)

    return {"added": added, "total_rows": total, "preview": df_new.head(10).to_dict(orient="records")}

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    df_upload = pd.read_csv(io.BytesIO(content))
    missing = [c for c in COLUMNS if c not in df_upload.columns]
    for m in missing:
        df_upload[m] = None
    df_upload = df_upload[COLUMNS]
    added, total = append_rows(df_upload)
    return {"merged_rows": len(df_upload), "total_rows": total}

@app.get("/download-csv")
async def download_csv():
    if not os.path.exists(DATASET_CSV):
        return {"error": "CSV not found"}
    with open(DATASET_CSV, "rb") as f:
        content = f.read().decode("utf-8", errors="ignore")
    return {"filename": os.path.basename(DATASET_CSV), "content": content}

@app.get("/columns")
async def get_columns():
    return {"columns": COLUMNS}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=PORT, reload=True)
