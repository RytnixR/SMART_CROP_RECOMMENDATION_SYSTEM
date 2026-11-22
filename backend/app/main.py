from pathlib import Path
import json, sqlite3
from datetime import datetime, timezone
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict

BASE = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE / "models" / "crop_model.joblib"
METRICS_PATH = BASE / "models" / "metrics.json"
DB_PATH = BASE / "data" / "history.db"
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

app = FastAPI(title="Smart Crop Recommendation API", version="1.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

class SoilInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    N: float = Field(ge=0, le=200)
    P: float = Field(ge=0, le=200)
    K: float = Field(ge=0, le=250)
    temperature: float = Field(ge=-5, le=60)
    humidity: float = Field(ge=0, le=100)
    ph: float = Field(ge=0, le=14)
    rainfall: float = Field(ge=0, le=1000)

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, crop TEXT NOT NULL,
        inputs TEXT NOT NULL, confidence REAL, created_at TEXT NOT NULL
    )""")
    con.commit()
    return con

@app.get("/api/health")
def health():
    return {"status": "ok", "model_ready": MODEL_PATH.exists()}

@app.get("/api/metrics")
def metrics():
    if not METRICS_PATH.exists():
        raise HTTPException(503, "Model metrics not found. Run backend/train_model.py first.")
    return json.loads(METRICS_PATH.read_text())

@app.post("/api/predict")
def predict(data: SoilInput):
    if not MODEL_PATH.exists():
        raise HTTPException(503, "Model not trained. Run python train_model.py in backend.")
    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    row = pd.DataFrame([[getattr(data, f) for f in FEATURES]], columns=FEATURES)
    crop = str(model.predict(row)[0])
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(max(model.predict_proba(row)[0]))
    created = datetime.now(timezone.utc).isoformat()
    con = connect()
    cur = con.execute(
        "INSERT INTO predictions(crop, inputs, confidence, created_at) VALUES(?,?,?,?)",
        (crop, data.model_dump_json(), confidence, created)
    )
    con.commit()
    item_id = cur.lastrowid
    con.close()
    return {"id": item_id, "crop": crop, "confidence": confidence, "model": bundle.get("model_name"), "created_at": created}

@app.get("/api/history")
def history(limit: int = 20):
    con = connect()
    rows = con.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT ?", (max(1, min(limit, 100)),)).fetchall()
    con.close()
    return [{"id": r["id"], "crop": r["crop"], "inputs": json.loads(r["inputs"]),
             "confidence": r["confidence"], "created_at": r["created_at"]} for r in rows]

@app.delete("/api/history")
def clear_history():
    con = connect()
    con.execute("DELETE FROM predictions")
    con.commit()
    con.close()
    return {"deleted": True}
