#import FastAPI from the fastAPI library
from fastapi import FastAPI
#check backend is running well and posting
from app.api.v1.routes_health import router as health_router
#routes images for prediction
from app.api.v1.routes_predictions import router as prediction_router
# import Base and engine from the session module in the db package
from app.db.session import Base, engine
# import models from the models module in the db package
from app.db import models
# import models router from the routes_model module in the api.v1 package
from app.api.v1.routes_model import router as models_router
# import models router from the routes_model module in the api.v1 package
from app.api.v1.routes_reviews import router as review_router
# import models router from the routes_model module in the api.v1 package
from app.api.v1.routes_metrics import router as metrics_router

Base.metadata.create_all(bind=engine)  # Create the database tables if they don't exist
#create FastAPI instance

app = FastAPI(
    title = "Mimi's Plants",
    description = "This is a plant disease detection API that uses a deep learning model to predict the disease of a plant based on an image of its leaves.",
    version = "1.0.0",
    )
#connect routers to app
app.include_router(health_router)
app.include_router(prediction_router)
app.include_router(review_router)
app.include_router(models_router)
app.include_router(metrics_router)
# use uvicorn to run the app with the command: python -m uvicorn app.main:app --reload
# use the following command to get into the correct directory:
    # cd cd C:\Users\{your user}\MimisGarden\backend\app (windows)
