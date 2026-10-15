import re
from typing import List, Dict, Any

class RuleSignalEngine:
    """
    Deterministic rule-based risk evaluation engine that detects established
    recruitment fraud indicators, phishing patterns, payment scams, and deceptive hiring language.
    """

    FINANCIAL_PATTERNS = [
        (
            r"\b(registration\s+fee|processing\s+fee|application\s+fee|onboarding\s+fee|training\s+fee)\b",
            "CRITICAL",
            "FINANCIAL",
            "Upfront Fee / Registration Charge Requested",
            "Legitimate employers never require candidates to pay an upfront registration, processing, or application fee.",
            35.0
        ),
        (
            r"\b(wire\s+transfer|western\s+union|moneygram|cashapp|zelle|crypto|bitcoin|usdt|gift\s+cards?)\b",
            "CRITICAL",
            "FINANCIAL",
            "Untraceable Payment Method Requested",
            "Mentions of cryptocurrency, wire transfers, Zelle, or gift cards in recruitment are definitive fraud signatures.",
            40.0
        ),
        (
            r"\b(deposit\s+a?\s*check|cash\s+the\s+check|reimburse|equipment\s+check|send\s+back\s+the\s+difference)\b",
            "CRITICAL",
            "FINANCIAL",
            "Counterfeit Check / Re-shipping Advance Scam",
            "Job requires depositing an employer check to purchase home office equipment and refunding the excess balance.",
            45.0
        ),
        (
            r"\b(security\s+deposit|refundable\s+deposit|pay\s+for\s+your\s+own\s+laptop|purchase\s+software\s+license)\b",
            "HIGH",
            "FINANCIAL",
            "Candidate Equipment / Software Purchase Demand",
            "Employers are legally obligated to supply or configure their own equipment without requiring upfront deposits.",
            30.0
        )
    ]

    CONTACT_PATTERNS = [
        (
            r"\b(telegram|t\.me/|reach\s+(?:out\s+|me\s+|us\s+)?on\s+telegram|interview\s+(?:on|via)\s+telegram|contact\s+@\w+)\b",
            "CRITICAL",
            "CONTACT",
            "Recruiter Telegram Communication Channel",
            "Scammers commonly conduct anonymous communication via Telegram or Signal to evade corporate oversight.",
            35.0
        ),
        (
            r"\b(whatsapp\s+only|chat\s+via\s+whatsapp|message\s+(?:us\s+|me\s+)?on\s+whatsapp\s*:\s*\+?\d+|whatsapp\s*:\s*\+?\d+)\b",
            "HIGH",
            "CONTACT",
            "Informal WhatsApp-Only Communication",
            "Reputable enterprises communicate through official corporate email domains and authenticated video platforms.",
            25.0
        ),
        (
            r"\b[A-Za-z0-9._%+-]+@(gmail|yahoo|hotmail|outlook|aol|protonmail)\.com\b",
            "MEDIUM",
            "CONTACT",
            "Free Webmail Used for Corporate Recruiting",
            "Job listing uses a free public email provider (e.g. @gmail, @yahoo) instead of a verified enterprise domain.",
            20.0
        )
    ]

    COMPENSATION_PATTERNS = [
        (
            r"\b(\$?\s*5000\s*(to|-)\s*\$?\s*10000\s*/\s*(week|wk)|earn\s+\$?\s*[3-9]\d{3}\s+weekly)\b",
            "HIGH",
            "COMPENSATION",
            "Unrealistic Weekly Compensation",
            "Promises exorbitant compensation ($3,000–$10,000/week) disproportionate to typical market rates.",
            25.0
        ),
        (
            r"\b(earn\s+\$?\d{2,3}\s*/\s*hr\s+no\s+experience|earn\s+quick\s+cash|unlimited\s+income\s+guaranteed)\b",
            "HIGH",
            "COMPENSATION",
            "High Hourly Pay with No Prerequisite Experience",
            "Claims substantial wages for unskilled or unspecified remote work with guaranteed instant returns.",
            25.0
        )
    ]

    URGENCY_AND_PROCESS_PATTERNS = [
        (
            r"\b(no\s+interview\s+needed|hired\s+immediately|start\s+working\s+today\s+without|no\s+resume\s+required)\b",
            "HIGH",
            "CONTENT",
            "Bypassed Interview / Instant Hiring Without Vetting",
            "Job claims candidate is hired immediately without technical screening, interview, or formal application review.",
            30.0
        ),
        (
            r"\b(kindly\s+(send|reply|forward|fill|wire)|urgent\s+vacancy\s+act\s+fast|limited\s+slots?\s+apply\s+now)\b",
            "MEDIUM",
            "CONTENT",
            "High-Pressure Tactics & Deceptive Terminology",
            "Phrasing exhibits unnatural urgency or distinct linguistic patterns frequently observed in scam communications.",
            15.0
        )
    ]

    SUSPICIOUS_ROLES = [
        (
            r"\b(package\s+(reshipment|forwarding)\s+agent|mystery\s+shopper|secret\s+evaluator|rebill\s+processor)\b",
            "CRITICAL",
            "CONTENT",
            "Known High-Risk Scam Job Profile",
            "Roles like 'package reshipper' or 'secret mystery shopper' are well-documented conduits for stolen goods and check fraud.",
            40.0
        )
    ]

    def evaluate(self, title: str, description: str, company: str, job_url: str = None) -> Dict[str, Any]:
        """
        Scans all text fields against threat patterns and calculates rule-based risk score.
        """
        combined_text = f"{title or ''} {company or ''} {description or ''}"
        detected_signals: List[Dict[str, Any]] = []
        raw_score = 0.0

        all_rules = (
            self.FINANCIAL_PATTERNS +
            self.CONTACT_PATTERNS +
            self.COMPENSATION_PATTERNS +
            self.URGENCY_AND_PROCESS_PATTERNS +
            self.SUSPICIOUS_ROLES
        )

        for pattern, severity, category, name, explanation, weight in all_rules:
            matches = list(re.finditer(pattern, combined_text, re.IGNORECASE))
            if matches:
                evidence_snippets = [m.group(0) for m in matches[:2]]
                evidence_str = f"Found matches: '{', '.join(evidence_snippets)}'"
                detected_signals.append({
                    "name": name,
                    "severity": severity,
                    "category": category,
                    "description": explanation,
                    "evidence": evidence_str
                })
                raw_score += weight

        # Heuristic checks on structural completeness
        desc_len = len((description or "").strip())
        if desc_len < 50:
            detected_signals.append({
                "name": "Extremely Sparse Description",
                "severity": "LOW",
                "category": "CONTENT",
                "description": "Legitimate corporate listings provide detailed responsibilities, qualifications, and role context.",
                "evidence": f"Description contains only {desc_len} characters."
            })
            raw_score += 10.0

        if not (company or "").strip():
            detected_signals.append({
                "name": "Anonymous / Unspecified Employer",
                "severity": "MEDIUM",
                "category": "COMPANY",
                "description": "The posting fails to disclose a clear legal hiring entity or corporate identity.",
                "evidence": "Employer name is empty or omitted."
            })
            raw_score += 15.0

        # Cap rule score to 100
        rule_score = min(round(raw_score, 1), 100.0)

        return {
            "rule_score": rule_score,
            "signals": detected_signals
        }

rule_engine = RuleSignalEngine()
