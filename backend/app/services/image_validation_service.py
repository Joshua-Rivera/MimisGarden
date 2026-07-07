# import BytesIO from the io module to handle in-memory binary streams
from io import BytesIO
#import image from the PIL module to handle image processing
from pathlib import Path
# import HTTPException and UploadFile from the fastapi module to handle HTTP exceptions and file uploads
from fastapi import HTTPException, UploadFile
# import Image and UnidentifiedImageError from the PIL module to handle image processing and exceptions related to unidentified images
from PIL import Image, UnidentifiedImageError

# Define a set of allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
#
MAX_FILE_SIZE_MB = 5  # Maximum file size in megabytes
#
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Maximum file size in bytes


async def validate_uploaded_image(file: UploadFile) -> tuple[bytes, str]:
    """
    Validate the uploaded image file.

    Args:
        file (UploadFile): The uploaded image file.

    Returns:
        tuple: A tuple containing the image bytes and the file extension.

    Raises:
        HTTPException: If the file is not a valid image or exceeds the maximum size.
    """
    # Check if the uploaded file has a valid extension
    original_filename = file.filename or ""
    file_extension = Path(original_filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}",
        )
    # Read the contents of the uploaded file
    contents = await file.read()
    # check if file is empty
    if len(contents) == 0:
        raise HTTPException(
            status_code=400, detail="Uploaded file is empty."
        )
    # check max size
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB.",
        )

    try:
        image = Image.open(BytesIO(contents))
        image.verify()  # Verify that the file is a valid image
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400, detail="Uploaded file is not a valid image."
        )
    return contents, file_extension