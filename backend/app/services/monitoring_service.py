from sqlalchemy import func # Importing the func module from SQLAlchemy for using SQL functions in queries
from sqlalchemy.orm import Session # Importing the Session class from SQLAlchemy for database session management
from app.db.models import PredictionLog #import log prediction log model class


def get_summary_metrics(db: Session):

    total_predictions = db.query(PredictionLog).count()  # Count the total number of predictions in the database

    average_confidence = db.query(func.avg(PredictionLog.confidence)).scalar()  # Calculate the average confidence of predictions

    needs_review_count = db.query(PredictionLog).filter(PredictionLog.needs_review == True).count()  # Count the number of predictions that need review
    # Calculate the review rate as the ratio of predictions needing review to total predictions
    review_rate = 0
    if total_predictions > 0:
        review_rate = (needs_review_count / total_predictions) 
    # Return a dictionary containing the summary metrics, including total predictions, average confidence, needs review count, and review rate
    return {
        "total_predictions": total_predictions,
        "average_confidence": round(
            average_confidence or 0,
            3
        ),
        "needs_review_count": needs_review_count,
        "review_rate": round(
            review_rate,
            3
        ),
    }

def get_prediction_metrics(db: Session):
    """
    Retrieve metrics for a specific prediction based on its ID.

    Args:
        db (Session): The database session.
        prediction_id (str): The ID of the prediction to retrieve metrics for.
    """

    average = (
        db.query(func.avg(PredictionLog.confidence))
        .scalar()
    )
    highest = (
        db.query(func.max(PredictionLog.confidence))
        .scalar()
    )
    lowest = (
        db.query(func.min(PredictionLog.confidence))
        .scalar()
    )

    return { "average_confidence": round(
            average or 0,
            3
        ),
        "highest_confidence": round(
            highest or 0,
            3
        ),
        "lowest_confidence": round(
            lowest or 0,
            3
        ),
    }

def get_label_metrics(db: Session):
    """
    Retrieve metrics related to the labels of predictions.

    Args:
        db (Session): The database session.
    """
    results = (
        db.query(
            PredictionLog.plant_state,
            func.count(PredictionLog.plant_state)
        )
        .group_by(PredictionLog.plant_state)
        .all()
    )

    labels = {}

    for label, count in results:
        labels[label] = count

    return {
        "labels": labels
    }


def get_review_metrics(db: Session):
    """
    Retrieve metrics related to predictions that need review.
    
    Args:
        db (Session): The database session.
    """
    total_predictions = (
        db.query(PredictionLog)
        .count()
    )

    total_reviews_needed = (
        db.query(PredictionLog)
        .filter(PredictionLog.needs_review == True)
        .count()
    )

    percentage = 0

    if total_predictions > 0:
        percentage = (
            total_reviews_needed /
            total_predictions
        )

    return {
        "total_reviews_needed": total_reviews_needed,
        "review_percentage": round(
            percentage,
            3
        ),
    }