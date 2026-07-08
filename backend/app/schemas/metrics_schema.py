from pydantic import BaseModel # Import basemodel for class metrics

class SummaryMetric(BaseModel):
    """
    Pydantic model for summarizing metrics related to the plant disease detection API.
    This model is used for data validation and serialization of summary metrics.
    """
    total_predictions: int
    average_confidence: float
    needs_review_count: int
    review_rate: int

class ConfidenceMetrics(BaseModel):
    """
    Pydantic model for summarizing confidence metrics related to the plant disease detection API.
    This model is used for data validation and serialization of confidence metrics.
    """
    average_confidence: float
    min_confidence: float
    max_confidence: float

class LabelMetrics(BaseModel):
    """
    Pydantic model for summarizing label metrics related to the plant disease detection API.
    This model is used for data validation and serialization of label metrics.
    """
    labels: dict[str, int]  # Dictionary mapping labels to their respective counts

class ReviewMetrics(BaseModel):
    """
    Pydantic model for summarizing review metrics related to the plant disease detection API.
    This model is used for data validation and serialization of review metrics.
    """
    total_reviews_needed: int
    review_percentage: int
    