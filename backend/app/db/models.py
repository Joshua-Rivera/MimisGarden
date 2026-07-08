# current date and time
from datetime import datetime
from typing import Text
# SQLAlchemy imports for defining database models
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship
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

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Timestamp for when the prediction was logged

class Review(Base):
    """
    Database model for storing reviews of predictions made by the plant disease detection API.
    This model allows users to provide feedback on the accuracy and usefulness of the predictions.
    """
    __tablename__ = "reviews"  # Name of the table in the database

    review_id = Column(String, primary_key=True, index=True)
    prediction_id = Column(String, 
                           ForeginKey("prediction_logs.prediction_id"),
                           nullable = False,
                           index = False) # Foreign key to PredictionLog (not enforced here)
    correct_label = Column(String, nullable=False)
    review_notes = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Timestamp for when the review was submitted
    prediction = relationship("PredictionLog")


##MACHINE LEARNING !!!! RAAHHH

class ModelMetadata(Base):
    """
    Database model for storing metadata about the machine learning models used in the plant disease detection API.
    This model helps track different versions of the models and their associated information.
    """
    __tablename__ = "model_metadata"  # Name of the table in the database

    model_id = Column(String, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    model_version = Column(String, nullable=False, unique=True, index=True)
    accuracy = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="experimental")    # e.g., "active", "deprecated"

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Timestamp for when the model metadata was created