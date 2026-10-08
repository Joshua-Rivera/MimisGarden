from fastapi import APIRouter, HTTPException
from app.ml.inference import load_model

router = APIRouter(tags=["models"])

@router.get("/models/current")
def get_current_model_endpoint():
    try:
        metadata = load_model()[3]
    except (RuntimeError, OSError, KeyError, ValueError) as exc:
        raise HTTPException(503, "A compatible trained model is not available") from exc
    return {"model_id": metadata["model_version"], "model_name": metadata["architecture"], "status": "active", **metadata}

@router.get("/models")
def read_all_models():
    return [get_current_model_endpoint()]
