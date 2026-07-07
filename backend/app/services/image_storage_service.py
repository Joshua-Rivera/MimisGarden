#importas path from the patthlib file for easy usage instead of just stringss :D
from pathlib import Path
#creates a random unique id for each image 
from uuid import uuid4
#imports the UploadFile class from FastAPI to handle file uploads in the API endpoints
from fastapi import UploadFile

from app.services.image_validation_service import validate_uploaded_image
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
    # Validate the uploaded image using the image validation service
    contents, file_extension = await validate_uploaded_image(file)
    # generate a unique image ID using uuid4 and append the file extension to create a unique filename for the uploaded image
    image_id = f"img_{uuid4().hex}{file_extension}"
    # create the full path for the image to be saved, combining the upload directory, unique image ID, and file extension
    image_path = UPLOAD_DIR / f"{image_id}{file_extension}"
    # write the contents of the uploaded image to the specified path
    with open(image_path, "wb") as image_file:
        image_file.write(contents)
    return str(image_path)  # Return the path to the saved image