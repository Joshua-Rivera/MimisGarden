#import router from fastapi library, to create routes
from fastapi import APIRouter

#router creates a container for endpoints (routes), and tags are used to group endpoints together in the documentation
router = APIRouter(tags=["health"])

#get endpoint creation for health check, this endpoint will be used to check if the API is running well and posting
@router.get("/health")
def check_health():
    """
    Check the health of the API.
    """
    return {"status": "ok",
            "service": "planthealth-api-check",
            "version": "1.0.0",}