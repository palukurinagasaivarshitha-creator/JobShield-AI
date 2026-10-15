from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.schemas.analysis import CompanyVerification
from app.services.domain_verifier import verify_company_and_domain

router = APIRouter()

class VerifyRequest(BaseModel):
    company_name: str = Field(..., min_length=1, description="Company name to verify")
    job_url: Optional[str] = Field(default=None, description="Job URL to corroborate with corporate domain")

@router.post("/verify", response_model=CompanyVerification, status_code=status.HTTP_200_OK, tags=["Verification"])
def verify_company(payload: VerifyRequest):
    """
    Independently inspects company domain registration, official career portals,
    and checks if the submitted vacancy URL is corroborated by verified infrastructure.
    """
    try:
        result = verify_company_and_domain(payload.company_name, payload.job_url)
        return CompanyVerification(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification inspection failed: {str(e)}"
        )
