FROM python:3.13-slim
WORKDIR /srv
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 STORAGE_DIR=/srv/storage MODEL_PATH=/srv/models/plant_model_v1.pt
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --timeout 60 --retries 3 -r requirements.txt
COPY backend/app ./app
RUN useradd --create-home garden && mkdir -p /srv/storage/uploaded_images /srv/models && chown -R garden:garden /srv
USER garden
COPY --chown=garden:garden backend/app/ml/models/plant_model_v1.pt /srv/models/plant_model_v1.pt
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
