from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator

class JobAnalysisRequest(BaseModel):
    job_title: Optional[str] = Field(default="", description="Job title, e.g. 'Senior Python Engineer'")
    company_name: Optional[str] = Field(default="", description="Company name, e.g. 'Google' or 'Meta'")
    job_description: Optional[str] = Field(default="", description="Full text description of the job posting")
    job_url: Optional[str] = Field(default=None, description="Direct URL of the job posting")

    @model_validator(mode="after")
    def validate_inputs(self):
        desc = (self.job_description or "").strip()
        url = (self.job_url or "").strip()
        if not desc and not url:
            raise ValueError("Either a valid job_url or a non-empty job_description must be provided.")
        return self


class DetectedSignal(BaseModel):
    name: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    category: str  # FINANCIAL, CONTACT, COMPENSATION, COMPANY, CONTENT, DOMAIN
    description: str
    evidence: Optional[str] = None


class CompanyVerification(BaseModel):
    status: str = "INCONCLUSIVE"  # VERIFIED, UNVERIFIED, MISMATCH, INCONCLUSIVE
    claimed_company: Optional[str] = None
    official_domain: Optional[str] = None
    domain_verified: bool = False
    official_career_url: Optional[str] = None
    official_apply_url: Optional[str] = None
    vacancy_verified: bool = False
    evidence: List[str] = Field(default_factory=list)
    notes: str = ""


class MLPredictionDetails(BaseModel):
    is_fake: bool
    confidence: float
    fraud_probability: float
    features_analyzed: List[str] = Field(default_factory=list)
    is_fallback: bool = False
    algorithm: str = "TF-IDF + Calibrated Classifier (EMSCAD trained)"


class AnalysisResponse(BaseModel):
    id: Optional[int] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    job_title: str
    company_name: str
    job_url: Optional[str] = None
    job_description_snippet: str = ""
    classification: str  # SAFE, SUSPICIOUS, HIGH_RISK
    risk_score: float    # 0.0 - 100.0
    risk_level_explanation: str
    ml_prediction: MLPredictionDetails
    detected_signals: List[DetectedSignal] = Field(default_factory=list)
    verification: CompanyVerification
    recommendations: List[str] = Field(default_factory=list)
    disclaimer: str = (
        "Notice: While this system uses machine learning trained on verified recruitment fraud patterns "
        "and multi-vector heuristic corroboration, a low-risk score does not guarantee employment authenticity. "
        "Always cross-reference vacancies on the employer's official website and never pay money for job offers."
    )


class JobUrlFetchRequest(BaseModel):
    url: str


class ScrapedJobData(BaseModel):
    title: str
    company: str
    description: str
    canonical_url: str
    source_domain: str
    meta_tags: dict = Field(default_factory=dict)
