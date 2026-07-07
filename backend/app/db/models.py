# current date and time
from datetime import datetime
# SQLAlchemy imports for defining database models
from sqlalchemy import Boolean, Column, DateTime, Float, String

from app.db.session import Base  # Import the Base class from the session module

class PredictionLog(Base):
    """
    Database model for logging predictions made by the plant disease detection API.
    This model stores information about each prediction, including the image path, timestamp, and prediction results.
    """
    __tablename__ = "prediction_logs"  # Name of the table in the database

    prediction_id = Column(String, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    plant_state = Column(String, nullable=False)
    possible_condition = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    suggestion = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    needs_review = Column(Boolean, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)