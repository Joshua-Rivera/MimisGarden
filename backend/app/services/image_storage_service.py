from uuid import uuid4
from fastapi import UploadFile
from app.core.config import UPLOAD_DIR
from app.services.image_validation_service import validate_uploaded_image

async def save_uploaded_image(file: UploadFile) -> str:
    contents, extension = await validate_uploaded_image(file)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = UPLOAD_DIR / f"img_{uuid4().hex}{extension}"
    path.write_bytes(contents)
    return str(path)
