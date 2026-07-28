from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ReviewSample(Base):
    __tablename__ = "review_samples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    prediction_id: Mapped[str] = mapped_column(String, nullable=False)

    image_path: Mapped[str] = mapped_column(String, nullable=False)

    predicted_label: Mapped[str] = mapped_column(String, nullable=False)

    corrected_label: Mapped[str | None] = mapped_column(String)

    confidence: Mapped[float] = mapped_column(Float)

    review_status: Mapped[str] = mapped_column(String, default="pending")

    approved_for_training: Mapped[bool] = mapped_column(Boolean, default=False)
