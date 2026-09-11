"""Load one trusted local checkpoint and use its exact label/preprocessing contract."""
import json
import threading
from functools import lru_cache
from pathlib import Path

import torch
from PIL import Image, ImageOps
from torch import nn
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights
from app.core.config import MODEL_PATH

_lock = threading.Lock()

@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.is_file():
        raise RuntimeError("No trained model is installed")
    checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    labels = json.loads((Path(__file__).parent / "labels.json").read_text())
    if checkpoint.get("architecture") != "efficientnet_b0":
        raise RuntimeError("The installed checkpoint is not EfficientNet-B0")
    if checkpoint.get("labels") != labels or checkpoint.get("class_to_idx") != {label: i for i, label in enumerate(labels)}:
        raise RuntimeError("Checkpoint labels do not match the application")
    if checkpoint.get("pretrained_weights") != "IMAGENET1K_V1" or checkpoint.get("image_size") != 224:
        raise RuntimeError("Unsupported checkpoint preprocessing")
    model = efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(labels))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    # CPU inference keeps the web process portable and avoids competing with training.
    return model, EfficientNet_B0_Weights.IMAGENET1K_V1.transforms(), labels, {
        "model_version": checkpoint["model_version"],
        "architecture": checkpoint["architecture"],
        "accuracy": checkpoint.get("validation_accuracy"),
        "f1_score": checkpoint.get("validation_f1"),
    }

def run_inference(image_path: str) -> dict:
    with _lock, torch.inference_mode():
        model, transform, labels, metadata = load_model()
        with Image.open(image_path) as image:
            tensor = transform(ImageOps.exif_transpose(image).convert("RGB")).unsqueeze(0)
        probabilities = model(tensor).softmax(dim=1)[0]
        index = int(probabilities.argmax())
        return {"plant_state": labels[index], "confidence": float(probabilities[index]), "model_version": metadata["model_version"]}
