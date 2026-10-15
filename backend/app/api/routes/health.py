import os
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health", tags=["System"])
def health_check():
    """
    Returns platform operational status, environment, and ML model availability.
    """
    model_exists = os.path.exists(settings.MODEL_PATH)
    dataset_exists = os.path.exists(settings.DATASET_PATH) or os.path.exists(settings.SEED_DATASET_PATH)
    
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "ml_model_loaded": model_exists,
        "dataset_available": dataset_exists,
        "database": "connected"
    }
