from pathlib import Path
import json

MODELS_DIR = Path(__file__).parent / "models"
REGISTRY_PATH = MODELS_DIR / "registry.json"


def load_registry() -> dict:
    """Load the model registry from the JSON file."""
    if not REGISTRY_PATH.exists():
        return {}
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)


def save_registry(registry: dict) -> None:
    """Save the model registry to the JSON file."""
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=4)
