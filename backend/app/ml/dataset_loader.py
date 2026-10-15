import csv
import logging
import os
from pathlib import Path
import pandas as pd
from app.core.config import settings

logger = logging.getLogger(__name__)

# Representative seed dataset modeled directly on verified EMSCAD recruitment fraud patterns & real job postings.
# Used for instant training, automated tests, and offline execution without requiring internet access.
SEED_DATA = [
    # Legitimate Job Postings (fraudulent = 0)
    {
        "title": "Senior Backend Python Engineer",
        "company_profile": "Acme Technologies is an enterprise cloud SaaS provider building distributed data streaming tools for Fortune 500 companies.",
        "description": "We are seeking a Senior Python Engineer to lead architecture for our scalable microservices. You will work with FastAPI, PostgreSQL, Kubernetes, and Kafka.",
        "requirements": "5+ years of software engineering experience with Python. Strong proficiency in asynchronous programming, relational databases, Docker, and CI/CD pipelines. Bachelor's degree in Computer Science or equivalent practical experience.",
        "benefits": "Competitive salary, 401(k) matching, comprehensive health insurance, flexible paid time off, and remote equipment allowance.",
        "telecommuting": 1,
        "has_company_logo": 1,
        "has_questions": 1,
        "employment_type": "Full-time",
        "required_experience": "Mid-Senior level",
        "required_education": "Bachelor's Degree",
        "industry": "Computer Software",
        "function": "Engineering",
        "fraudulent": 0
    },
    {
        "title": "Lead Frontend React Developer",
        "company_profile": "FinStream is a modern fintech platform processing millions of secure global payments daily.",
        "description": "Design and maintain high-performance web dashboards using modern React, TypeScript, and state management. Collaborate closely with product managers and UX designers to craft intuitive interfaces.",
        "requirements": "Demonstrated expertise in React, modern JavaScript, web accessibility (WCAG), CSS architectures, and frontend automated testing (Jest, Cypress).",
        "benefits": "Competitive equity package, medical, dental, vision coverage, annual learning stipend, and wellness budget.",
        "telecommuting": 0,
        "has_company_logo": 1,
        "has_questions": 1,
        "employment_type": "Full-time",
        "required_experience": "Mid-Senior level",
        "required_education": "Bachelor's Degree",
        "industry": "Financial Services",
        "function": "Engineering",
        "fraudulent": 0
    },
    {
        "title": "Data Scientist - Machine Learning",
        "company_profile": "BioAnalytics Inc conducts genomic research and develops predictive diagnostic algorithms for clinical research institutions.",
        "description": "Develop supervised and unsupervised machine learning models to detect bio-markers in high-dimensional tabular and image data. Build reproducible training pipelines using Scikit-learn and PyTorch.",
        "requirements": "MS or PhD in Statistics, Computer Science, or Data Science. Hands-on experience with feature engineering, model evaluation, cross-validation, and productionizing ML models.",
        "benefits": "Competitive compensation, comprehensive benefits package, 401(k) with company match, and on-site gym.",
        "telecommuting": 0,
        "has_company_logo": 1,
        "has_questions": 1,
        "employment_type": "Full-time",
        "required_experience": "Associate",
        "required_education": "Master's Degree",
        "industry": "Biotechnology",
        "function": "Research",
        "fraudulent": 0
    },
    {
        "title": "DevOps & Cloud Security Architect",
        "company_profile": "Apex Cloud Systems provides secure infrastructure management and compliance automation for federal and private organizations.",
        "description": "Responsible for managing AWS infrastructure via Terraform, establishing zero-trust IAM policies, administering Kubernetes clusters, and automating security scanning.",
        "requirements": "Solid experience with AWS, Terraform, Docker, Kubernetes, Linux system administration, and security vulnerability management.",
        "benefits": "Competitive salary, annual bonus, full healthcare coverage, life insurance, and remote work flexibility.",
        "telecommuting": 1,
        "has_company_logo": 1,
        "has_questions": 1,
        "employment_type": "Full-time",
        "required_experience": "Director",
        "required_education": "Bachelor's Degree",
        "industry": "Information Technology and Services",
        "function": "Information Technology",
        "fraudulent": 0
    },
    {
        "title": "Human Resources Specialist",
        "company_profile": "GreenLeaf Retail operates sustainable consumer goods outlets across North America.",
        "description": "Coordinate employee onboarding, manage benefits administration, assist with talent acquisition, and ensure organizational compliance with labor standards.",
        "requirements": "Bachelor's degree in Human Resources or Business. 2+ years of HR experience. Excellent interpersonal and conflict resolution skills.",
        "benefits": "Medical, dental, retirement plan with match, generous employee discount, and paid vacation.",
        "telecommuting": 0,
        "has_company_logo": 1,
        "has_questions": 0,
        "employment_type": "Full-time",
        "required_experience": "Entry level",
        "required_education": "Bachelor's Degree",
        "industry": "Retail",
        "function": "Human Resources",
        "fraudulent": 0
    },
    {
        "title": "Customer Support Representative",
        "company_profile": "CloudHost Global provides domain registration, web hosting, and technical DNS support to small businesses worldwide.",
        "description": "Provide responsive omnichannel technical assistance to customers via ticketing systems, live chat, and scheduled voice calls. Troubleshoot DNS and email routing issues.",
        "requirements": "Previous experience in customer service or tech support. Strong written communication skills and patience when explaining technical concepts.",
        "benefits": "Health and dental coverage, paid training, flexible shift scheduling, and retirement contributions.",
        "telecommuting": 1,
        "has_company_logo": 1,
        "has_questions": 1,
        "employment_type": "Full-time",
        "required_experience": "Entry level",
        "required_education": "High School or equivalent",
        "industry": "Internet",
        "function": "Customer Service",
        "fraudulent": 0
    },
    {
        "title": "Senior Product Marketing Manager",
        "company_profile": "DataPulse builds enterprise business intelligence platforms helping retailers optimize their inventory turnover.",
        "description": "Define product positioning, craft compelling customer-facing collateral, plan product launches, and lead competitive research.",
        "requirements": "5+ years in B2B SaaS product marketing. Proven track record of successful cross-functional product launches and sales enablement.",
        "benefits": "Performance bonuses, comprehensive health plans, 401(k), and paid parental leave.",
        "telecommuting": 1,
        "has_company_logo": 1,
        "has_questions": 1,
        "employment_type": "Full-time",
        "required_experience": "Mid-Senior level",
        "required_education": "Bachelor's Degree",
        "industry": "Marketing and Advertising",
        "function": "Marketing",
        "fraudulent": 0
    },
    {
        "title": "Associate Accountant",
        "company_profile": "Heritage Financial Consultants is an accounting and tax advisory firm serving regional businesses for 35 years.",
        "description": "Prepare month-end journal entries, reconcile bank and ledger accounts, assist with quarterly payroll filings, and support tax audit preparations.",
        "requirements": "Degree in Accounting or Finance. Working knowledge of QuickBooks and Excel (vlookups, pivot tables). CPA candidate preferred.",
        "benefits": "Health insurance, paid CPA study materials and exam fees, retirement contribution, and annual performance incentive.",
        "telecommuting": 0,
        "has_company_logo": 1,
        "has_questions": 1,
        "employment_type": "Full-time",
        "required_experience": "Entry level",
        "required_education": "Bachelor's Degree",
        "industry": "Accounting",
        "function": "Accounting/Auditing",
        "fraudulent": 0
    },

    # Fraudulent Job Postings (fraudulent = 1) - Replicating classic EMSCAD scams
    {
        "title": "Data Entry Clerk / Work From Home ($45/hr)",
        "company_profile": "",
        "description": "URGENT HIRING: We are looking for data entry clerks to start work immediately from home. Earn $45 per hour with flexible hours. You will receive an upfront check to buy equipment. Send your resume to hr-recruiting-department@gmail.com and contact our hiring manager on Telegram at @recruiter_mark.",
        "requirements": "No experience needed! Anyone can apply. Must have internet access and an active bank account to deposit your equipment check.",
        "benefits": "Earn $5,000 to $10,000 per week. Daily payouts via Western Union or Bitcoin. Immediate start without interview.",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "employment_type": "Part-time",
        "required_experience": "Not Applicable",
        "required_education": "Unspecified",
        "industry": "Telecommunications",
        "function": "Administrative",
        "fraudulent": 1
    },
    {
        "title": "Package Forwarding Logistics Assistant",
        "company_profile": "Global Express Logistics is looking for home inspection agents.",
        "description": "Receive packages at your residential address, inspect the contents, re-package them, and ship them to overseas addresses using provided prepaid shipping labels. Earn $3,500 monthly. You will be sent money orders or wire transfers for operational expenses.",
        "requirements": "Must be home to receive deliveries. Must be willing to forward packages within 24 hours of arrival.",
        "benefits": "High commission per forwarded package. No interview required. Kindly contact us via WhatsApp immediately.",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "employment_type": "Contract",
        "required_experience": "Entry level",
        "required_education": "High School or equivalent",
        "industry": "Logistics and Supply Chain",
        "function": "Supply Chain",
        "fraudulent": 1
    },
    {
        "title": "Secret Mystery Shopper & Quality Evaluator",
        "company_profile": "",
        "description": "Evaluate local retail stores and money transfer services. We will send you a cashier's check for $2,950. You will deposit the check in your personal bank account, keep $450 as your compensation, and evaluate Western Union or MoneyGram by wiring the remaining $2,500 to our verification agent.",
        "requirements": "Must have an active checking account in good standing. Honest and reliable candidates only.",
        "benefits": "Keep $450 per assignment. Multiple assignments available weekly.",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "employment_type": "Temporary",
        "required_experience": "Not Applicable",
        "required_education": "Unspecified",
        "industry": "Consumer Services",
        "function": "Other",
        "fraudulent": 1
    },
    {
        "title": "Junior Crypto Operations Trainee (Registration Fee Required)",
        "company_profile": "Blockchain Elite Investments manages high-frequency digital currency portfolios.",
        "description": "Assist our crypto trading desk with trade confirmations. Successful candidates must pay a one-time refundable registration fee of $150 in USDT or Bitcoin for background check and trading terminal certification. Once paid, daily earnings of $800 are guaranteed.",
        "requirements": "Must own a cryptocurrency wallet (TrustWallet or MetaMask). Fast typing and willingness to follow trading instructions.",
        "benefits": "Guaranteed daily payouts in Bitcoin. Act fast, only 3 positions left today!",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "employment_type": "Contract",
        "required_experience": "Entry level",
        "required_education": "Unspecified",
        "industry": "Financial Services",
        "function": "Finance",
        "fraudulent": 1
    },
    {
        "title": "Administrative Assistant - Microsoft Remote Team",
        "company_profile": "Alleged Microsoft Partner Recruitment Office.",
        "description": "Microsoft is urgently seeking remote administrative assistants. Selected candidates will be hired on the spot. Kindly download Telegram and message our hiring coordinator at @msft_career_desk for your text interview. Do not apply through standard portals as this is a private recruitment link.",
        "requirements": "Basic typing skills. Must have a smartphone with Telegram installed.",
        "benefits": "$85/hour with full benefits from day one.",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "employment_type": "Full-time",
        "required_experience": "Entry level",
        "required_education": "Unspecified",
        "industry": "Information Technology and Services",
        "function": "Administrative",
        "fraudulent": 1
    },
    {
        "title": "Online Rebilling & Payment Processing Representative",
        "company_profile": "",
        "description": "Receive payments from our international clients directly into your personal bank account or CashApp, deduct your 10% commission, and remit the rest via Bitcoin ATM within 2 hours. Start working today without any interview.",
        "requirements": "Active bank account or Zelle account. Fast communication.",
        "benefits": "Make up to $3,000 in your first week.",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "employment_type": "Part-time",
        "required_experience": "Not Applicable",
        "required_education": "Unspecified",
        "industry": "Financial Services",
        "function": "Accounting/Auditing",
        "fraudulent": 1
    }
]


def ensure_seed_dataset(output_path: str = None) -> str:
    """
    Creates seed dataset file if not present on disk.
    """
    path = output_path or settings.SEED_DATASET_PATH
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        logger.info(f"Writing seed dataset with EMSCAD patterns to {path}...")
        df = pd.DataFrame(SEED_DATA)
        df.to_csv(path, index=False)
    
    return path


def load_dataset(dataset_path: str = None) -> pd.DataFrame:
    """
    Loads full EMSCAD dataset if available, otherwise loads the validated seed dataset.
    Performs data cleaning, imputation, and column normalization.
    """
    target_path = dataset_path or settings.DATASET_PATH
    
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        logger.info(f"Loading full dataset from {target_path}")
        df = pd.read_csv(target_path)
    else:
        seed_path = ensure_seed_dataset()
        logger.info(f"Target dataset '{target_path}' not found. Loading validated seed dataset from {seed_path}")
        df = pd.read_csv(seed_path)

    # Impute missing values
    text_columns = ["title", "company_profile", "description", "requirements", "benefits"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)
        else:
            df[col] = ""

    # Ensure target column exists
    if "fraudulent" not in df.columns:
        raise ValueError("Dataset does not contain the required target column: 'fraudulent'")

    df["fraudulent"] = df["fraudulent"].fillna(0).astype(int)

    # Combine text features to create unified corpus representation
    df["combined_text"] = (
        df["title"] + " " +
        df["company_profile"] + " " +
        df["description"] + " " +
        df["requirements"]
    ).str.strip()

    return df

if __name__ == "__main__":
    df = load_dataset()
    print(f"Dataset successfully loaded. Total rows: {len(df)}")
    print(f"Class breakdown:\n{df['fraudulent'].value_counts()}")
