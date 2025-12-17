from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from pathlib import Path
import joblib
import pandas as pd

app = FastAPI(title="IDS FastAPI")


class PredictRequest(BaseModel):
    rows: List[Dict[str, Any]]


MODEL_PATH = Path("database") / "rf_model.joblib"
model = None
if MODEL_PATH.exists():
    try:
        model = joblib.load(MODEL_PATH)
    except Exception:
        model = None


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        df = pd.DataFrame(req.rows)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input format: {e}")

    try:
        preds = model.predict(df)
        result = {"predictions": preds.tolist()}
        if hasattr(model, "predict_proba"):
            result["probabilities"] = model.predict_proba(df).tolist()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reload-model")
def reload_model():
    global model
    if not MODEL_PATH.exists():
        raise HTTPException(status_code=404, detail=f"Model file not found at {MODEL_PATH}")
    try:
        model = joblib.load(MODEL_PATH)
        return {"status": "reloaded", "model_loaded": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
