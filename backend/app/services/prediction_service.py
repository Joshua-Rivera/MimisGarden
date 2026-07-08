#used to assign a unique identifier to each prediction request / image
from uuid import uuid4
# used to handle file uploads in the API endpoints
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.db.models import PredictionLog
#import functions for model predictions, such as how to apply confidence level and care suggestions and model inference, and image services
from app.core.care_suggestions import get_care_suggestion
from app.core.confidence_rules import apply_confidence_rules
from app.ml.inference import run_inference
from app.services.image_storage_service import save_uploaded_image

async def create_prediction(file: UploadFile, db: Session) -> dict:
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

    care_result = get_care_suggestion(plant_state)
    # generates unique id per prediction
    prediction_id = f"pred_{uuid4().hex}"
    #formats responses to include the following in a json format
    prediction_response = {
        "prediction_id": prediction_id,
        "plant_state": plant_state,
        "possible_condition": care_result["condition"],
        "confidence": raw_prediction["confidence"],
        "severity": care_result["severity"],
        "suggestion": care_result["suggestion"],
        "model_version": raw_prediction["model_version"],
        "needs_review": needs_review,
    }
    #logs the json response to the database for future reference
    prediction_log = PredictionLog(
        prediction_id=prediction_id,
        image_path=image_path,
        plant_state=plant_state,
        possible_condition=care_result["condition"],
        confidence=raw_prediction["confidence"],
        severity=care_result["severity"],
        suggestion=care_result["suggestion"],
        model_version=raw_prediction["model_version"],
        needs_review=needs_review,
    )

    db.add(prediction_log)
    db.commit()

    return prediction_response
