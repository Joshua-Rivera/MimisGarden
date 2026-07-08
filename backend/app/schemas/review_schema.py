from datetime import datetime #tells the time duh
# Pydantic schema for review data class
from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    """
    Pydantic schema for creating a review.
    """
    correct_label: str
    review_notes: str | None = None

class ReviewResponse(BaseModel):
    """
    Pydantic schema for the response of a review.
    """
    review_id: str
    prediction_id: str
    correct_label: str
    review_notes: str | None
    reviewed_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Config to allow attribute access for ORM models