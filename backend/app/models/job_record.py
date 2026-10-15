import json
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from app.database.session import Base

class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    job_title = Column(String(255), nullable=False, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    job_url = Column(Text, nullable=True)
    job_description = Column(Text, nullable=False)
    classification = Column(String(50), nullable=False, index=True)  # SAFE, SUSPICIOUS, HIGH_RISK
    risk_score = Column(Float, nullable=False)  # 0.0 to 100.0
    ml_risk_score = Column(Float, nullable=False, default=0.0)
    rule_risk_score = Column(Float, nullable=False, default=0.0)
    is_fallback = Column(Boolean, default=False)
    
    # Serialized JSON representations
    _signals = Column("signals", Text, default="[]")
    company_verification_status = Column(String(50), default="INCONCLUSIVE")
    official_domain = Column(String(255), nullable=True)
    official_career_url = Column(Text, nullable=True)
    official_apply_url = Column(Text, nullable=True)
    vacancy_verified = Column(Boolean, default=False)
    _verification_evidence = Column("verification_evidence", Text, default="[]")
    _recommendations = Column("recommendations", Text, default="[]")

    @property
    def signals(self):
        try:
            return json.loads(self._signals or "[]")
        except Exception:
            return []

    @signals.setter
    def signals(self, value):
        self._signals = json.dumps(value or [])

    @property
    def verification_evidence(self):
        try:
            return json.loads(self._verification_evidence or "[]")
        except Exception:
            return []

    @verification_evidence.setter
    def verification_evidence(self, value):
        self._verification_evidence = json.dumps(value or [])

    @property
    def recommendations(self):
        try:
            return json.loads(self._recommendations or "[]")
        except Exception:
            return []

    @recommendations.setter
    def recommendations(self, value):
        self._recommendations = json.dumps(value or [])


class JobSearchListing(Base):
    __tablename__ = "job_search_listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False)
    salary_range = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    source = Column(String(100), default="Public Careers Index")
    official_domain = Column(String(255), nullable=True)
    official_apply_url = Column(Text, nullable=True)
    is_verified_posting = Column(Boolean, default=True)
    initial_risk_estimate = Column(String(50), default="SAFE")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
