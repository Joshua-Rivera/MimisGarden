from io import BytesIO
from pathlib import Path
import warnings
from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

async def validate_uploaded_image(file: UploadFile) -> tuple[bytes, str]:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Choose a JPG, PNG, or WebP image")
    contents = await file.read(MAX_FILE_SIZE_BYTES + 1)
    if not contents:
        raise HTTPException(400, "Uploaded file is empty")
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(413, "Images must be 5 MB or smaller")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(contents)) as image:
                if image.format not in {"JPEG", "PNG", "WEBP"}:
                    raise ValueError("Unsupported image encoding")
                if image.width * image.height > 20_000_000:
                    raise ValueError("Image exceeds 20 megapixels")
                image.verify()
            with Image.open(BytesIO(contents)) as image:
                image.load()
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(400, "The image is damaged, unsupported, or too large")
    return contents, extension
