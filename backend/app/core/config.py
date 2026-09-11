"""Deployment settings. Paths do not depend on the launch directory."""
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2]
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", str(BACKEND_DIR / "storage"))).resolve()
UPLOAD_DIR = STORAGE_DIR / "uploaded_images"
MODEL_PATH = Path(os.getenv("MODEL_PATH", str(BACKEND_DIR / "app/ml/models/plant_model_v1.pt"))).resolve()
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{STORAGE_DIR / 'planthealth.db'}")
