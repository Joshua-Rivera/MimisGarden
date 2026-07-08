
from fastapi import APIRouter, Depends, File, UploadFile

from sqlalchemy.orm import Session
from app.db.models import PredictionLog
# import prediction responses and created predictions for endpoint functionality
from app.schemas.prediction_schema import PredictionResponse
from app.services.prediction_service import create_prediction
# import get_db from the session module in the db package to manage database sessions
from app.db.session import get_db
# Routes predictions through the API endpoints, allowing users to upload images and receive predictions about plant health.
router = APIRouter(prefix="/api/v1", tags=["predictions"])

# creates a POST endpoint at /api/v1/predict that accepts an image file upload and returns a prediction response.
#  The endpoint uses the create_prediction function to process the uploaded image and generate a prediction.
@router.post("/predict", response_model=PredictionResponse)
async def predict_plant_health(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Endpoint to predict plant health from an uploaded image.

    Args:
        file (UploadFile): The uploaded image file.
    """
    return await create_prediction(file, db)

@router.get("/predictions")
def get_predictions(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all predictions from the database.

    Args:
        db (Session): The database session.
    """
    predictions = db.query(PredictionLog).order_by(PredictionLog.created_at.desc()).all()
    return predictions
