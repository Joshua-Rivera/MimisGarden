from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class ReviewCreate(BaseModel):
    correct_label: Literal["healthy", "leaf_spots", "severe_damage", "uncertain"]
    review_notes: str | None = Field(default=None, max_length=2000)

class ReviewResponse(BaseModel):
    review_id: str
    prediction_id: str
    correct_label: str
    review_notes: str | None
    reviewed_at: datetime
    model_config = ConfigDict(from_attributes=True)
