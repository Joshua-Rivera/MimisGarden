
from fastapi import APIRouter, File, UploadFile
# import prediction responses and created predictions for endpoint functionality
from app.schemas.prediction_schema import PredictionResponse
from app.services.prediction_service import create_prediction
# Routes predictions through the API endpoints, allowing users to upload images and receive predictions about plant health.
router = APIRouter(prefix="/api/v1", tags=["predictions"])

# creates a POST endpoint at /api/v1/predict that accepts an image file upload and returns a prediction response.
#  The endpoint uses the create_prediction function to process the uploaded image and generate a prediction.
@router.post("/predict", response_model=PredictionResponse)
async def predict_plant_health(file: UploadFile = File(...)):
    """
    Endpoint to predict plant health from an uploaded image.

    Args:
        file (UploadFile): The uploaded image file.
    """
    return await create_prediction(file)