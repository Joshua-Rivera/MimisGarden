#imports basemodel from pydantic in order to validate data, defining how 
# the data should look like in a response, and the types of each field in the response
from pydantic import BaseModel

class PredictionResponse(BaseModel):
    prediction: str
    plant_state: str
    possible_condition: str
    confidence: float
    severity: str
    suggestion: str
    model_version: str
    needs_attention: bool