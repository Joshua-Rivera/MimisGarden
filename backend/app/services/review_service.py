from datetime import UTC, datetime
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import Review, PredictionLog
from app.schemas.review_schema import ReviewCreate


def get_review_queue(db: Session):
    return db.query(PredictionLog).filter(PredictionLog.needs_review.is_(True)).order_by(PredictionLog.created_at.desc()).limit(100).all()


def create_review(db: Session, review_data: ReviewCreate, prediction_id: str):
    prediction = db.get(PredictionLog, prediction_id)
    if prediction is None:
        raise HTTPException(404, "Prediction not found")
    review = db.query(Review).filter(Review.prediction_id == prediction_id).first()
    if review is None:
        review = Review(review_id=str(uuid4()), prediction_id=prediction_id)
        db.add(review)
    review.correct_label = review_data.correct_label
    review.review_notes = review_data.review_notes
    review.reviewed_at = datetime.now(UTC).replace(tzinfo=None)
    prediction.needs_review = False
    db.commit()
    db.refresh(review)
    return review
