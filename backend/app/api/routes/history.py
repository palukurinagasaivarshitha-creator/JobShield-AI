from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.session import get_db
from app.models.job_record import JobAnalysis
from app.schemas.analysis import AnalysisResponse, DetectedSignal, CompanyVerification, MLPredictionDetails

router = APIRouter()

def record_to_schema(r: JobAnalysis) -> AnalysisResponse:
    signals_data = [DetectedSignal(**s) for s in r.signals]
    verification_data = CompanyVerification(
        status=r.company_verification_status or "INCONCLUSIVE",
        claimed_company=r.company_name,
        official_domain=r.official_domain,
        domain_verified=bool(r.official_domain and r.company_verification_status == "VERIFIED"),
        official_career_url=r.official_career_url,
        official_apply_url=r.official_apply_url,
        vacancy_verified=r.vacancy_verified,
        evidence=r.verification_evidence or [],
        notes="Historical verified record."
    )
    ml_data = MLPredictionDetails(
        is_fake=r.risk_score >= 50.0,
        confidence=round(r.risk_score / 100.0 if r.risk_score >= 50 else (100.0 - r.risk_score) / 100.0, 3),
        fraud_probability=round(r.risk_score / 100.0, 3),
        features_analyzed=["historical_audit_record"],
        is_fallback=r.is_fallback,
        algorithm="TF-IDF + Calibrated Classifier"
    )

    return AnalysisResponse(
        id=r.id,
        timestamp=r.created_at.isoformat() if r.created_at else "",
        job_title=r.job_title,
        company_name=r.company_name,
        job_url=r.job_url,
        job_description_snippet=(r.job_description[:250] + "...") if len(r.job_description) > 250 else r.job_description,
        classification=r.classification,
        risk_score=r.risk_score,
        risk_level_explanation=f"Historic evaluation logged with status {r.classification}.",
        ml_prediction=ml_data,
        detected_signals=signals_data,
        verification=verification_data,
        recommendations=r.recommendations or []
    )


@router.get("", response_model=List[AnalysisResponse], tags=["History"])
def get_analysis_history(
    q: Optional[str] = Query(None, description="Search company or job title"),
    classification: Optional[str] = Query(None, description="Filter by SAFE, SUSPICIOUS, HIGH_RISK"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retrieves chronological audit logs of all past job scans.
    """
    query = db.query(JobAnalysis)

    if q:
        search_filter = f"%{q.strip()}%"
        query = query.filter(
            (JobAnalysis.job_title.ilike(search_filter)) |
            (JobAnalysis.company_name.ilike(search_filter))
        )

    if classification:
        query = query.filter(JobAnalysis.classification == classification.upper())

    records = query.order_by(desc(JobAnalysis.created_at)).offset(offset).limit(limit).all()
    return [record_to_schema(r) for r in records]


@router.get("/{analysis_id}", response_model=AnalysisResponse, tags=["History"])
def get_analysis_detail(analysis_id: int, db: Session = Depends(get_db)):
    """
    Retrieves complete multi-vector report for a specific scan ID.
    """
    record = db.query(JobAnalysis).filter(JobAnalysis.id == analysis_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis report with ID {analysis_id} not found."
        )
    return record_to_schema(record)


@router.delete("/{analysis_id}", status_code=status.HTTP_200_OK, tags=["History"])
def delete_analysis_record(analysis_id: int, db: Session = Depends(get_db)):
    """
    Removes a scan record from the database.
    """
    record = db.query(JobAnalysis).filter(JobAnalysis.id == analysis_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis report with ID {analysis_id} not found."
        )
    db.delete(record)
    db.commit()
    return {"message": f"Analysis report {analysis_id} deleted successfully."}
