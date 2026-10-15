from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.session import get_db
from app.models.job_record import JobAnalysis, JobSearchListing
from app.schemas.job import JobListingOut, DashboardStatsOut

router = APIRouter()

# Initial seed listings representing documented genuine corporate openings and sample scam patterns
SAMPLE_SEARCH_LISTINGS = [
    {
        "title": "Software Engineer, Infrastructure",
        "company": "Google",
        "location": "Mountain View, CA (Hybrid)",
        "salary_range": "$140,000 - $190,000 / yr",
        "description": "Develop next-generation infrastructure technologies that change how billions of users connect, explore, and interact with information. Work on distributed storage systems and planetary-scale computing.",
        "requirements": "BS degree in Computer Science or equivalent practical experience. Experience with Unix/Linux environments, C++, Java, or Python.",
        "source": "Official Employer Portal",
        "official_domain": "google.com",
        "official_apply_url": "https://careers.google.com",
        "is_verified_posting": True,
        "initial_risk_estimate": "SAFE"
    },
    {
        "title": "Cloud Support Associate",
        "company": "Amazon",
        "location": "Seattle, WA",
        "salary_range": "$95,000 - $130,000 / yr",
        "description": "Act as a technical liaison between AWS customers and engineering teams. Resolve complex technical issues spanning cloud architecture, networking, and virtualization.",
        "requirements": "Bachelor's degree in Information Science or equivalent. Experience with Linux or Windows system administration and TCP/IP networking.",
        "source": "Official Employer Portal",
        "official_domain": "amazon.com",
        "official_apply_url": "https://www.amazon.jobs",
        "is_verified_posting": True,
        "initial_risk_estimate": "SAFE"
    },
    {
        "title": "Senior Frontend Engineer - Streaming UI",
        "company": "Netflix",
        "location": "Los Gatos, CA (Remote)",
        "salary_range": "$220,000 - $350,000 / yr",
        "description": "Architect and deliver high-performance streaming web experiences across millions of living room devices. Optimize rendering pipelines and state management.",
        "requirements": "7+ years software engineering experience. Deep mastery of JavaScript/TypeScript, React, performance profiling, and browser rendering internals.",
        "source": "Official Employer Portal",
        "official_domain": "netflix.com",
        "official_apply_url": "https://jobs.netflix.com",
        "is_verified_posting": True,
        "initial_risk_estimate": "SAFE"
    },
    {
        "title": "Full Stack Developer",
        "company": "Microsoft",
        "location": "Redmond, WA",
        "salary_range": "$125,000 - $175,000 / yr",
        "description": "Build user-friendly web interfaces and robust cloud backends for Microsoft 365 services. Collaborate with design and product teams on modern productivity tools.",
        "requirements": "Experience with modern web frameworks (React, Angular), C# or Node.js, and Azure cloud infrastructure.",
        "source": "Official Employer Portal",
        "official_domain": "microsoft.com",
        "official_apply_url": "https://careers.microsoft.com",
        "is_verified_posting": True,
        "initial_risk_estimate": "SAFE"
    },
    {
        "title": "Immediate Data Entry Clerk ($65/hr)",
        "company": "Global Logistics Hub",
        "location": "Remote / Anywhere",
        "salary_range": "$65/hr ($5,200/wk)",
        "description": "Urgent opening for remote data entry. Hired immediately without interview. We send you an upfront equipment check to purchase home office supplies. Contact recruiter on Telegram @instant_jobs_desk.",
        "requirements": "No experience needed. Active bank account required to deposit company equipment check.",
        "source": "Unverified 3rd Party Feed",
        "official_domain": "unknown-jobs.xyz",
        "official_apply_url": None,
        "is_verified_posting": False,
        "initial_risk_estimate": "HIGH_RISK"
    },
    {
        "title": "Mystery Shopper & Wire Evaluator",
        "company": "Retail Quality Audits",
        "location": "Remote / Flexible",
        "salary_range": "$800 per evaluation",
        "description": "Test local wire transfer services like Western Union. Receive cashier check, deposit in personal bank, keep commission and wire the balance to our security auditor.",
        "requirements": "Personal bank account. Fast response time.",
        "source": "Unverified Classifieds",
        "official_domain": "audit-eval.top",
        "official_apply_url": None,
        "is_verified_posting": False,
        "initial_risk_estimate": "HIGH_RISK"
    }
]


def ensure_seed_job_listings(db: Session):
    count = db.query(JobSearchListing).count()
    if count == 0:
        for item in SAMPLE_SEARCH_LISTINGS:
            db_item = JobSearchListing(**item)
            db.add(db_item)
        db.commit()


@router.get("/search", response_model=List[JobListingOut], tags=["Jobs"])
def search_jobs(
    q: Optional[str] = Query(None, description="Keywords for job title, company, or skills"),
    classification: Optional[str] = Query(None, description="Filter by SAFE, SUSPICIOUS, or HIGH_RISK"),
    limit: int = Query(12, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Search authenticated and documented job listings.
    Allows testing verified official vacancy apply links alongside flagged scam listings.
    """
    ensure_seed_job_listings(db)
    query = db.query(JobSearchListing)

    if q:
        search_filter = f"%{q.strip()}%"
        query = query.filter(
            (JobSearchListing.title.ilike(search_filter)) |
            (JobSearchListing.company.ilike(search_filter)) |
            (JobSearchListing.description.ilike(search_filter))
        )

    if classification:
        query = query.filter(JobSearchListing.initial_risk_estimate == classification.upper())

    results = query.order_by(JobSearchListing.id.asc()).offset(offset).limit(limit).all()
    
    return [
        JobListingOut(
            id=item.id,
            title=item.title,
            company=item.company,
            location=item.location,
            salary_range=item.salary_range,
            description=item.description,
            requirements=item.requirements,
            source=item.source,
            official_domain=item.official_domain,
            official_apply_url=item.official_apply_url,
            is_verified_posting=item.is_verified_posting,
            initial_risk_estimate=item.initial_risk_estimate,
            created_at=item.created_at.isoformat() if item.created_at else ""
        )
        for item in results
    ]


@router.get("/dashboard/stats", response_model=DashboardStatsOut, tags=["Dashboard"])
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Returns platform-wide analysis statistics and recent checks for the dashboard overview.
    """
    total_scans = db.query(JobAnalysis).count()
    safe_count = db.query(JobAnalysis).filter(JobAnalysis.classification == "SAFE").count()
    suspicious_count = db.query(JobAnalysis).filter(JobAnalysis.classification == "SUSPICIOUS").count()
    high_risk_count = db.query(JobAnalysis).filter(JobAnalysis.classification == "HIGH_RISK").count()
    verified_vacancies_count = db.query(JobAnalysis).filter(JobAnalysis.vacancy_verified == True).count()

    recent_records = (
        db.query(JobAnalysis)
        .order_by(desc(JobAnalysis.created_at))
        .limit(6)
        .all()
    )

    avg_score = 0.0
    if total_scans > 0:
        scores = [r.risk_score for r in db.query(JobAnalysis.risk_score).all()]
        avg_score = round(sum(scores) / len(scores), 1)

    recent_checks = [
        {
            "id": r.id,
            "job_title": r.job_title,
            "company_name": r.company_name,
            "classification": r.classification,
            "risk_score": r.risk_score,
            "created_at": r.created_at.isoformat() if r.created_at else "",
            "vacancy_verified": r.vacancy_verified,
            "official_apply_url": r.official_apply_url
        }
        for r in recent_records
    ]

    return DashboardStatsOut(
        total_scans=total_scans,
        safe_count=safe_count,
        suspicious_count=suspicious_count,
        high_risk_count=high_risk_count,
        verified_vacancies_count=verified_vacancies_count,
        average_risk_score=avg_score,
        recent_checks=recent_checks
    )
