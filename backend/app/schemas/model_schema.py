from datetime import datetime

from pydantic import BaseModel, ConfigDict

class ModelMetaDataResponse(BaseModel):
    """
    Pydantic model for representing the response schema of model metadata.
    This model is used to validate and serialize the data returned by the API when querying model metadata.
    """
    model_id: str
    model_name: str
    model_version: str
    accuracy: float | None = None
    f1_score: float | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)  # Allow population of the model from ORM objects