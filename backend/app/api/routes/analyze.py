import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.analysis import JobAnalysisRequest, AnalysisResponse, JobUrlFetchRequest, ScrapedJobData
from app.services.analyzer_service import analyze_job
from app.services.scraper import extract_job_from_url

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_200_OK, tags=["Analysis"])
def analyze_job_posting(request: JobAnalysisRequest, db: Session = Depends(get_db)):
    """
    Submits a job posting for multi-vector threat detection:
    - Analyzes text via ML trained on EMSCAD recruitment fraud patterns.
    - Evaluates heuristic fraud signatures (payments, untraceable chats, unrealistic compensation).
    - Checks official company domain legitimacy and vacancy corroboration.
    - Persists audit record to history.
    """
    try:
        response = analyze_job(request, db=db)
        return response
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while evaluating the job posting. Please check your inputs and try again."
        )


@router.post("/extract", response_model=ScrapedJobData, status_code=status.HTTP_200_OK, tags=["Analysis"])
def extract_url_data(payload: JobUrlFetchRequest):
    """
    Safely retrieves and parses job metadata from an external URL with SSRF protection.
    """
    try:
        extracted = extract_job_from_url(payload.url)
        return ScrapedJobData(**extracted)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Unable to safely retrieve content from URL: {str(e)}"
        )
