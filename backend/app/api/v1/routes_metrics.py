from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.metrics_schema import SummaryMetric, ConfidenceMetrics, LabelMetrics, ReviewMetrics

from app.services.monitoring_service import get_summary_metrics, get_confidence_metrics, get_label_metrics, get_review_metrics

router = APIRouter(
    tags=["metrics"]
)

@router.get(
    "/metrics/summary",
    response_model=SummaryMetric
)
def summary_metrics(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve summary metrics for predictions.

    Args:
        db (Session): The database session.
    Returns:
        SummaryMetric: A Pydantic model containing summary metrics.
    """
    return get_summary_metrics(db)

@router.get(
    "/metrics/confidence",
    response_model=ConfidenceMetrics
)
def confidence_metrics(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve confidence metrics for predictions.

    Args:
        db (Session): The database session.
    Returns:
        ConfidenceMetrics: A Pydantic model containing confidence metrics.
    """
    return get_confidence_metrics(db)

@router.get(
    "/metrics/labels",
    response_model=LabelMetrics
)
def label_metrics(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve label metrics for predictions.

    Args:
        db (Session): The database session.
    Returns:
        LabelMetrics: A Pydantic model containing label metrics.
    """
    return get_label_metrics(db)

@router.get(
    "/metrics/reviews",
    response_model=ReviewMetrics
)
def review_metrics(db: Session = Depends(get_db)):  
    """
    Endpoint to retrieve review metrics for predictions.

    Args:
        db (Session): The database session.
    Returns:
        ReviewMetrics: A Pydantic model containing review metrics.
    """
    return get_review_metrics(db)