from fastapi import APIRouter, Depends # Import APIRouter and Depends for creating API routes and handling dependencies
from sqlalchemy.orm import Session # Import Session for database session management

from app.db.session import get_db # Import the database session dependency
from app.schemas.prediction_schema import PredictionResponse # Import the PredictionLogResponse schema
from app.schemas.review_schema import ReviewCreate, ReviewResponse # Import the ReviewCreate and ReviewResponse schemas
from app.services.review_service import create_review, get_review_queue # Import the service functions for creating and retrieving reviews

router = APIRouter(tags=["reviews"]) # Create an APIRouter instance for defining API routes

@router.get("/reviews", response_model=list[PredictionResponse]) # Define a GET endpoint for retrieving the review queue
def list_review_queue(db: Session = Depends(get_db)): # Define the function to handle the GET request, with a database session dependency
    """
    Retrieve a list of predictions that need to be reviewed.
    This endpoint returns predictions that have been flagged for review, allowing users to provide feedback on their accuracy.
    """
    return get_review_queue(db) # Call the service function to get the review queue and return the results

@router.post("/reviews/{prediction_id}", response_model=ReviewResponse) # Define a POST endpoint for submitting a review
def submit_review(prediction_id: str, review_data: ReviewCreate, db: Session = Depends(get_db)): # Define the function to handle the POST request, with a database session dependency
    """
    Submit a review for a specific prediction.
    This endpoint allows users to provide feedback on the accuracy and usefulness of a prediction by submitting a review.
    """
    return create_review(prediction_id=prediction_id, review_data=review_data, db=db) # Call the service function to create a new review and return the result
