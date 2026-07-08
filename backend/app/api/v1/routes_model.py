from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.model_schema import ModelMetaDataResponse
from app.services.model_service import get_all_models, get_current_model


router = APIRouter(tags=["models"]);

@router.get("/models/current", response_model=ModelMetaDataResponse)
def get_current_model_endpoint(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve the current active machine learning model's metadata.
    """
    return get_current_model(db)

@router.get("/models", response_model=list[ModelMetaDataResponse])
def read_all_models(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all machine learning models' metadata.
    """
    return get_all_models(db)