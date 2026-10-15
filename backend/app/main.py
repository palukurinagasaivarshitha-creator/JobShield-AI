import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database.session import init_db
from app.api.router import api_router
from app.ml.pipeline import load_trained_model
from app.ml.dataset_loader import ensure_seed_dataset

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("app_main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle management.
    Initializes database tables, verifies seed datasets, and checks ML pipeline.
    """
    logger.info("Starting up Fake Job Detection & Verification Platform backend...")
    
    # 1. Initialize database schema
    try:
        init_db()
        logger.info("Database schema verified and initialized.")
    except Exception as e:
        logger.error(f"Database initialization warning: {e}")

    # 2. Ensure seed dataset is present
    try:
        ensure_seed_dataset()
    except Exception as e:
        logger.warning(f"Could not verify seed dataset: {e}")

    # 3. Check ML model
    model = load_trained_model()
    if model is None:
        logger.info("ML model artifact not found on startup. Triggering initial training...")
        try:
            from app.ml.train import train_and_save
            train_and_save()
            load_trained_model()
            logger.info("Initial ML model trained and loaded successfully.")
        except Exception as e:
            logger.warning(f"Initial model training deferred: {e}. Deterministic fallback mode active.")
    else:
        logger.info("Pre-trained ML model loaded and ready for inference.")

    yield

    logger.info("Shutting down Fake Job Detection Platform backend...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Full-Stack Machine Learning & Threat Intelligence API for Detecting Recruitment Fraud, "
        "Scam Postings, and Verifying Official Company Career Vacancies."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error processing {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred while processing your request."}
    )


# Attach routes
app.include_router(api_router, prefix="/api")


@app.get("/", tags=["Root"])
def root_endpoint():
    return {
        "platform": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "documentation": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
