from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.metrics_schema import SummaryMetric, ConfidenceMetrics, LabelMetrics, ReviewMetrics

from app.services.monitoring_service import get_summary_metrics, get_confidence_metrics, get_label_metrics, get_review_metrics

router = APIRouter(
    tags=["metrics"]
)