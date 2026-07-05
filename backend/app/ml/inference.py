#fake inference

def run_inference(image_path: str) -> str:
    return {
        "plant_state" : "dry_wilting",
        "confidence" : 0.082,
        "model_version" : "plant-health-v0-fake",
    }