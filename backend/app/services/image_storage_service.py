#importas path from the patthlib file for easy usage instead of just stringss :D
from pathlib import Path
#creates a random unique id for each image 
from uuid import uuid4
#imports the UploadFile class from FastAPI to handle file uploads in the API endpoints
from fastapi import UploadFile

#creates folder path for where the uploaded images will reside
UPLOAD_DIR = Path("storage/uploaded_images")
#creates the uploads folder if it does not exist already, allowing for nested directories to be created as needed
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
#specifies allowed file types 
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


async def save_uploaded_image(file: UploadFile) -> str:
    """
    Save an uploaded image to the server.

    Args:
        file (UploadFile): The uploaded image file.

    Returns:
        str: The path to the saved image.
    """
    original_filename = file.filename or ""

    file_extension = Path(original_filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        file_extension = ".jpg"  # Default to .jpg if the extension is not allowed
    
    image_id = f"img_{uuid4().hex}"

    image_path = UPLOAD_DIR / f"{image_id}{file_extension}"

    contents = await file.read()

    with open(image_path, "wb") as image_file:
        image_file.write(contents)

    return str(image_path)