from pathlib import Path  # import path for easy use for system
from typing import TypedDict


# model result class
class InferenceResult(TypedDict):
    plant_state: str
    confidence: float
    model_version: str


# Model Version
MODEL_VERSION = "plant-health-v0-fake"


def run_inference(image_path: str) -> str:
    "return model prediction for a given image"
    image_path = Path(image_path)
    if not image_path.is_file() or not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    return {
        "plant_state": "healthy",
        "confidence": 0.5,
        "model_version": MODEL_VERSION,
    }
