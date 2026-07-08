from datetime import datetime
from uuid import uuid4 #assign speficic unique id to request

from fastapi import HTTPException #http error exception import
from sqlalchemy.orm import Session # import the Session class from SQLAlchemy for database interactions
from app.db.models import Review, PredictionLog #import the Review and PredictionLog models from the models module
from app.schemas.review_schema import ReviewCreate 

def get_review_queue(db: Session) -> list[PredictionLog]:
    """
    Retrieve all predictions that need review from the database.

    Args:
        db (Session): The SQLAlchemy database session.
    """

    return (db.query(PredictionLog)
        .filter(PredictionLog.needs_review == True)
        .order_by(PredictionLog.created_at.desc())
        .all())

def create_review(db: Session, review_data: ReviewCreate, prediction_id: str) -> Review:
    """
    Create a new review for a specific prediction.

    Args:
        db (Session): The SQLAlchemy database session.
        review_data (ReviewCreate): The data for the new review.
        prediction_id (str): The ID of the prediction being reviewed.

    Raises:
        HTTPException: If the prediction with the given ID does not exist.

    Returns:
        Review: The newly created review object.
    """
    # Check if the prediction exists
    prediction = (
        db.query(PredictionLog)
        .filter(PredictionLog.prediction_id == prediction_id)
        .first())
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    # Create a new review instance
    new_review = Review(
        review_id=str(uuid4()),  # Generate a unique ID for the review
        prediction_id=prediction_id,
        correct_label=review_data.correct_label,
        review_notes=review_data.review_notes,
        reviewed_at=datetime.utcnow()  # Set the current UTC time as the review timestamp
    )

    # Add the new review to the database session and commit
    db.add(new_review)
    db.commit()
    db.refresh(new_review)  # Refresh to get the updated state from the database
    if prediction is not None:
        prediction.needs_review = False  # Mark the prediction as reviewed
        db.commit()  # Commit the change to the database
        db.refresh(prediction)  # Refresh to get the updated state from the database
    return new_review
