from uuid import uuid4 #assigns unique id to each request

from sqlalchemy.orm import Session

from app.db.models import ModelMetadata

DEFAULT_MODEL_NAME = "plant_health_classifier"
DEFAULT_MODEL_VERSION = "1.0.0"

def ensure_default_model_exists(db:Session) -> ModelMetadata:
    """
    Ensures that a default model metadata entry exists in the database.
    If it doesn't exist, creates a new entry with default values.
    
    Args:
        db (Session): SQLAlchemy database session.
    
    Returns:
        ModelMetadata: The existing or newly created model metadata entry.
    """
    # Check if the default model already exists in the database
    existing_model = (
        db.query(ModelMetadata)
        .filter_by(model_name=DEFAULT_MODEL_NAME, model_version=DEFAULT_MODEL_VERSION)
        .first())
    
    if existing_model is not None:
        return existing_model  # Return the existing model if found
        # If the default model does not exist, create a new entry
    default_model = ModelMetadata(
        model_id=str(uuid4()),  # Generate a unique ID for the model
        model_name=DEFAULT_MODEL_NAME,
        model_version=DEFAULT_MODEL_VERSION,
        accuracy=None,  # Accuracy can be set later after evaluation
        f1_score=None,  # F1 score can be set later after evaluation
        status="active"  # Default status is set to "active"
    )
    db.add(default_model)  # Add the new model to the session
    db.commit()     # Commit the transaction to save changes to the database
    db.refresh(default_model)  # Refresh the instance to get updated data from the database
    
    return default_model  # Return the existing or newly created model metadata entry


def get_current_model(db:Session) -> ModelMetadata:
    """
    Retrieves the current active model metadata entry from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
    
    Returns:
        ModelMetadata: The current active model metadata entry.
    """
    # Query the database for the current active model
    current_model = (
        db.query(ModelMetadata)
        .filter(ModelMetadata.status == "active")
        .first())
    
    if current_model is not  None:
        # If no active model is found, ensure the default model exists and return it
        return current_model
    
    return ensure_default_model_exists(db)  # Return the default model if no active model is found



def get_all_models(db:Session) -> list[ModelMetadata]:
    """
    Retrieves all model metadata entries from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
    
    Returns:
        list[ModelMetadata]: A list of all model metadata entries.
    """
    return (db.query(ModelMetadata)
            .order_by(ModelMetadata.created_at.desc())
            .all() ) # Query and return all model metadata entries
