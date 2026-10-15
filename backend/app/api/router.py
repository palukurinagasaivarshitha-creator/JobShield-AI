from fastapi import APIRouter
from app.api.routes import health, analyze, verify, jobs, history

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(analyze.router)
api_router.include_router(verify.router)
api_router.include_router(jobs.router, prefix="/jobs")
api_router.include_router(history.router, prefix="/history")
