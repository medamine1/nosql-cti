import joblib
from pathlib import Path

MODEL_PATH = Path("ml") / "model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception:
    model = None
