"""Mimi's Garden API. Run from backend with uvicorn app.main:app."""
import os
import logging
import time
from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_predictions import router as prediction_router
from app.api.v1.routes_reviews import router as review_router
from app.api.v1.routes_model import router as models_router
from app.api.v1.routes_metrics import router as metrics_router
from app.db.session import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Mimi's Garden", description="Visual plant-condition classification: healthy, leaf spots, or severe damage. Not a disease diagnosis.", version="1.0.0")
app.include_router(health_router)
app.include_router(prediction_router)
for router in (review_router, models_router, metrics_router):
    app.include_router(router, prefix="/api/v1")
    # Keep existing unversioned clients compatible.
    app.include_router(router, include_in_schema=False)
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500,http://localhost:5173,https://mimis-garden.vercel.app").split(","), allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])


@app.middleware("http")
async def record_request(request, call_next):
    started = time.perf_counter()
    request_id = uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    if request.url.path.startswith(("/api/", "/reviews", "/metrics")):
        response.headers["Cache-Control"] = "no-store"
    logging.getLogger("uvicorn.error").info("request_id=%s method=%s path=%s status=%s duration_ms=%.1f", request_id, request.method, request.url.path, response.status_code, (time.perf_counter() - started) * 1000)
    return response
