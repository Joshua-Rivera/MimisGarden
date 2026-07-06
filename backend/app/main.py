#import FastAPI from the fastAPI library
from fastapi import FastAPI
#check backend is running well and posting
from app.api.v1.routes_health import router as health_router
#routes images for prediction
from app.api.v1.routes_predictions import router as prediction_router

#create FastAPI instance

app = FastAPI(
    title = "Mimi's Plants",
    description = "This is a plant disease detection API that uses a deep learning model to predict the disease of a plant based on an image of its leaves.",
    version = "1.0.0",
    )
#connect health state to app and connect predictions to app
app.include_router(health_router)
app.include_router(prediction_router)


# use uvicorn to run the app with the command: python -m uvicorn app.main:app --reload
# use the following command to get into the correct directory:
    # cd cd C:\Users\{your user}\MimisGarden\backend\app (windows)
