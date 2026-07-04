def apply_confidence_rules(predicted_label: str, confidence: str, confidence: float) -> tuple[str, bool]:
    
    if confidence < 0.50:
        return "uncertain", True
    if predicted_label == "uncertain":
        return "uncertain", True
    if confidence < 0.70:
        return predicted_label, True
    return predicted_label, False