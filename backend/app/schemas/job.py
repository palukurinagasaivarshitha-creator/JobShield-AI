from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class JobSearchQuery(BaseModel):
    query: Optional[str] = None
    classification: Optional[str] = None
    limit: int = 12
    offset: int = 0

class JobListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    location: str
    salary_range: Optional[str] = None
    description: str
    requirements: Optional[str] = None
    source: str
    official_domain: Optional[str] = None
    official_apply_url: Optional[str] = None
    is_verified_posting: bool
    initial_risk_estimate: str
    created_at: str

class DashboardStatsOut(BaseModel):
    total_scans: int
    safe_count: int
    suspicious_count: int
    high_risk_count: int
    verified_vacancies_count: int
    average_risk_score: float
    recent_checks: List[dict]
