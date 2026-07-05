#used to assign a unique identifier to each prediction request / image
from uuid import uuid4
# used to handle file uploads in the API endpoints
from fastapi import UploadFile
#import functions for model predictions, such as how to apply confidence level and care suggestions and model inference, and image services
from app.core.care_suggestions import get_care_suggestions  
from app.core.confidence_rules import apply_confidence_rules
from app.ml.inference import run_inference
from app.services.image_storage_service import save_uploaded_image

async def create_prediction(file: UploadFile) -> dict:
    """
    Create a prediction for the uploaded image.

    Args:
        file (UploadFile): The uploaded image file.
    """
    #saves uploaded file to the server and returns the path to the saved image
    image_path = await save_uploaded_image(file)
    raw_prediction = run_inference(image_path)
    # applies confidence rules to the raw prediction to determine the plant state and whether the prediction needs review
    plant_state, needs_review = apply_confidence_rules(
        predicted_label=raw_prediction["plant_state"],
        confidence=raw_prediction["confidence"],
    )

    care_result = get_care_suggestions(plant_state)
    ## returns JSON response with prediction details, including a unique prediction ID, plant state, possible condition, confidence level, severity, care suggestion, model version, and whether the prediction needs review.
    return {
         "prediction_id": f"pred_{uuid4().hex}",
        "plant_state": plant_state,
        "possible_condition": care_result["condition"],
        "confidence": raw_prediction["confidence"],
        "severity": care_result["severity"],
        "suggestion": care_result["suggestion"],
        "model_version": raw_prediction["model_version"],
        "needs_review": needs_review,
    }
