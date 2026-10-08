from fastapi import APIRouter, HTTPException
from app.ml.inference import load_model
router = APIRouter(tags=["health"])

@router.get("/health")
def check_health():
    return {"status": "ok", "service": "mimis-garden"}

@router.get("/ready")
def readiness():
    try:
        metadata = load_model()[3]
    except Exception as exc:
        raise HTTPException(503, "Trained model unavailable") from exc
    return {"status": "ready", "model_version": metadata["model_version"]}
