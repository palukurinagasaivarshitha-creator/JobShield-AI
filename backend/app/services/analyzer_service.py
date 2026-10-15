import logging
import re
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.job_record import JobAnalysis
from app.schemas.analysis import (
    JobAnalysisRequest,
    AnalysisResponse,
    DetectedSignal,
    CompanyVerification,
    MLPredictionDetails
)
from app.services.domain_verifier import verify_company_and_domain
from app.services.rule_engine import rule_engine
from app.services.scraper import extract_job_from_url
from app.ml.pipeline import predict_job

logger = logging.getLogger(__name__)


def generate_recommendations(classification: str, signals: list, verification: dict) -> list[str]:
    recs = []
    if classification == "HIGH_RISK":
        recs.append("DO NOT send money, pay registration fees, or purchase equipment under any circumstances.")
        recs.append("Cease communication immediately if the recruiter requests communication solely on Telegram, Signal, or WhatsApp.")
        recs.append("Do not share sensitive personal information (Social Security / National ID, bank details, passport scans).")
        recs.append("Report this fraudulent posting to the relevant job board and your local cybercrime reporting agency.")
    elif classification == "SUSPICIOUS":
        recs.append("Independently cross-reference this job opening on the company's verified website before submitting personal details.")
        recs.append("Confirm the recruiter reaches out from a matching corporate email domain rather than a free email provider.")
        recs.append("Request a formal video interview conducted on standard enterprise platforms (Google Meet, Teams, Zoom).")
    else:
        recs.append("This job posting displays standard legitimate characteristics with no active threat indicators.")
        recs.append("Always apply directly through the employer's official careers portal whenever available.")
        recs.append("Remain cautious of any subsequent requests for payments or confidential financial data.")

    if verification.get("status") == "MISMATCH":
        recs.append("CRITICAL: The website domain does NOT belong to the claimed employer. Beware of lookalike phishing domains.")
    elif verification.get("official_career_url"):
        recs.append(f"Explore verified openings directly at: {verification.get('official_career_url')}")

    return recs


def infer_known_company(title: str, description: str) -> str:
    """Return a canonical name only when a known registry company is named in text.

    A textual mention is not verification; the verifier still marks the vacancy
    unverified unless a submitted URL can be corroborated.
    """
    from app.services.domain_verifier import KNOWN_ENTERPRISE_REGISTRY

    text = f"{title or ''}\n{description or ''}"
    for key, details in KNOWN_ENTERPRISE_REGISTRY.items():
        # Match whole words so short names (for example, Meta) do not match
        # arbitrary substrings inside unrelated words.
        pattern = r"(?i)(?<![\w])" + re.escape(key) + r"(?![\w])"
        if re.search(pattern, text):
            return details.get("canonical_name", key.title())
    return ""


def analyze_job(request: JobAnalysisRequest, db: Optional[Session] = None) -> AnalysisResponse:
    """
    Executes comprehensive multi-stage job analysis:
    1. Safe URL extraction & metadata parsing (if URL provided)
    2. Official company domain & vacancy verification
    3. Rule-based threat pattern detection
    4. Machine learning classification
    5. Composite risk scoring & database storage
    """
    title = (request.job_title or "").strip()
    company = (request.company_name or "").strip()
    description = (request.job_description or "").strip()
    job_url = (request.job_url or "").strip() or None

    # Step 1: Scrape if URL is provided and description is empty or user requested scraping
    if job_url and (not description or not title or not company):
        try:
            scraped = extract_job_from_url(job_url)
            if not title:
                title = scraped.get("title", "")
            if not company:
                company = scraped.get("company", "")
            if not description:
                description = scraped.get("description", "")
        except Exception as e:
            logger.warning(f"URL extraction note: {e}")
            if not description:
                description = f"Content could not be automatically retrieved from URL ({str(e)}). Assessed on URL heuristics."

    # Fallback placeholders for empty fields
    if not title:
        title = "Job Opportunity"
    if not company:
        company = "Unspecified Employer"

    # Step 2: Domain Verification
    verification_dict = verify_company_and_domain(company, job_url)

    # Step 3: Rule-based Signal Detection
    rule_results = rule_engine.evaluate(title, description, company, job_url)
    rule_score = rule_results["rule_score"]
    detected_signals = [DetectedSignal(**s) for s in rule_results["signals"]]

    # Step 4: Machine Learning Inference
    ml_results = predict_job(title, description, company)
    ml_score = ml_results["risk_score"]

    # Step 5: Composite Risk Calculation
    # If domain mismatch is detected, enforce heavy penalty
    domain_penalty = 0.0
    if verification_dict.get("status") == "MISMATCH":
        domain_penalty = 40.0
        detected_signals.insert(0, DetectedSignal(
            name="Domain Impersonation / Phishing Risk",
            severity="CRITICAL",
            category="DOMAIN",
            description=f"The job URL does not match the official domain of {company}.",
            evidence=f"Claimed company official domain is '{verification_dict.get('official_domain')}', but posting is on a different domain."
        ))

    # Weighting: Combine ML confidence, rule indicators, and domain verification
    has_critical_signal = any(s.severity == "CRITICAL" for s in detected_signals)
    if detected_signals:
        weighted = (ml_score * 0.30) + (rule_score * 0.70) + domain_penalty
        if has_critical_signal or rule_score >= 55.0:
            composite_score = max(weighted, rule_score + domain_penalty)
        else:
            composite_score = weighted
    else:
        composite_score = (ml_score * 0.70) + domain_penalty

    composite_score = min(round(composite_score, 1), 100.0)

    # Classification thresholding:
    # Any posting with critical threat indicators (fees, wire fraud, telegram interview, domain spoofing) is HIGH_RISK
    if composite_score >= 65.0 or (has_critical_signal and rule_score >= 45.0):
        classification = "HIGH_RISK"
        explanation = "High risk of fraudulent recruitment scam. Threat indicators detected (such as advance fee demands, untraceable contact methods, or domain impersonation)."
    elif composite_score >= 35.0:
        classification = "SUSPICIOUS"
        explanation = "Suspicious signals or domain anomalies detected. Exercise elevated diligence and verify directly with the employer."
    else:
        classification = "SAFE"
        explanation = "Low threat probability. Standard corporate hiring language and structural parameters observed."

    recommendations = generate_recommendations(classification, detected_signals, verification_dict)

    # Step 6: Persist in Database
    created_id = None
    should_close_db = False
    if db is None:
        db = SessionLocal()
        should_close_db = True

    try:
        record = JobAnalysis(
            job_title=title[:255],
            company_name=company[:255],
            job_url=job_url,
            job_description=description[:10000],
            classification=classification,
            risk_score=composite_score,
            ml_risk_score=ml_score,
            rule_risk_score=rule_score,
            is_fallback=ml_results.get("is_fallback", False),
            company_verification_status=verification_dict.get("status", "INCONCLUSIVE"),
            official_domain=verification_dict.get("official_domain"),
            official_career_url=verification_dict.get("official_career_url"),
            official_apply_url=verification_dict.get("official_apply_url"),
            vacancy_verified=verification_dict.get("vacancy_verified", False),
        )
        record.signals = [s.model_dump() for s in detected_signals]
        record.verification_evidence = verification_dict.get("evidence", [])
        record.recommendations = recommendations

        db.add(record)
        db.commit()
        db.refresh(record)
        created_id = record.id
    except Exception as e:
        logger.error(f"Error persisting analysis to database: {e}")
        db.rollback()
    finally:
        if should_close_db:
            db.close()

    # Step 7: Format Response
    verification_schema = CompanyVerification(**verification_dict)
    ml_schema = MLPredictionDetails(**ml_results)

    return AnalysisResponse(
        id=created_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        job_title=title,
        company_name=company,
        job_url=job_url,
        job_description_snippet=(description[:250] + "...") if len(description) > 250 else description,
        classification=classification,
        risk_score=composite_score,
        risk_level_explanation=explanation,
        ml_prediction=ml_schema,
        detected_signals=detected_signals,
        verification=verification_schema,
        recommendations=recommendations
    )
