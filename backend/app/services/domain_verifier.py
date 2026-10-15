import logging
import re
import socket
from urllib.parse import urlparse
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Verified enterprise registry with canonical domains, careers portals, and search templates
KNOWN_ENTERPRISE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "google": {
        "canonical_name": "Google LLC",
        "official_domain": "google.com",
        "career_url": "https://careers.google.com",
        "allowed_hosts": ["google.com", "careers.google.com", "google.co.in", "google.co.uk"],
        "ats_domains": []
    },
    "alphabet": {
        "canonical_name": "Alphabet Inc.",
        "official_domain": "abc.xyz",
        "career_url": "https://careers.google.com",
        "allowed_hosts": ["abc.xyz", "google.com", "careers.google.com"],
        "ats_domains": []
    },
    "microsoft": {
        "canonical_name": "Microsoft Corporation",
        "official_domain": "microsoft.com",
        "career_url": "https://careers.microsoft.com",
        "allowed_hosts": ["microsoft.com", "careers.microsoft.com", "jobs.careers.microsoft.com"],
        "ats_domains": []
    },
    "amazon": {
        "canonical_name": "Amazon.com, Inc.",
        "official_domain": "amazon.com",
        "career_url": "https://www.amazon.jobs",
        "allowed_hosts": ["amazon.com", "amazon.jobs", "www.amazon.jobs"],
        "ats_domains": []
    },
    "apple": {
        "canonical_name": "Apple Inc.",
        "official_domain": "apple.com",
        "career_url": "https://jobs.apple.com",
        "allowed_hosts": ["apple.com", "jobs.apple.com"],
        "ats_domains": []
    },
    "meta": {
        "canonical_name": "Meta Platforms, Inc.",
        "official_domain": "meta.com",
        "career_url": "https://www.metacareers.com",
        "allowed_hosts": ["meta.com", "metacareers.com", "www.metacareers.com", "facebook.com"],
        "ats_domains": []
    },
    "netflix": {
        "canonical_name": "Netflix, Inc.",
        "official_domain": "netflix.com",
        "career_url": "https://jobs.netflix.com",
        "allowed_hosts": ["netflix.com", "jobs.netflix.com"],
        "ats_domains": ["jobs.lever.co/netflix"]
    },
    "ibm": {
        "canonical_name": "IBM",
        "official_domain": "ibm.com",
        "career_url": "https://www.ibm.com/careers",
        "allowed_hosts": ["ibm.com", "www.ibm.com"],
        "ats_domains": []
    },
    "cisco": {
        "canonical_name": "Cisco Systems",
        "official_domain": "cisco.com",
        "career_url": "https://jobs.cisco.com",
        "allowed_hosts": ["cisco.com", "jobs.cisco.com"],
        "ats_domains": []
    },
    "oracle": {
        "canonical_name": "Oracle Corporation",
        "official_domain": "oracle.com",
        "career_url": "https://www.oracle.com/corporate/careers/",
        "allowed_hosts": ["oracle.com", "www.oracle.com"],
        "ats_domains": []
    },
    "adobe": {
        "canonical_name": "Adobe Inc.",
        "official_domain": "adobe.com",
        "career_url": "https://www.adobe.com/careers.html",
        "allowed_hosts": ["adobe.com", "www.adobe.com"],
        "ats_domains": []
    },
    "salesforce": {
        "canonical_name": "Salesforce, Inc.",
        "official_domain": "salesforce.com",
        "career_url": "https://www.salesforce.com/company/careers/",
        "allowed_hosts": ["salesforce.com", "careers.salesforce.com"],
        "ats_domains": []
    },
    "spotify": {
        "canonical_name": "Spotify Technology S.A.",
        "official_domain": "spotify.com",
        "career_url": "https://www.lifeatspotify.com",
        "allowed_hosts": ["spotify.com", "lifeatspotify.com", "www.lifeatspotify.com"],
        "ats_domains": []
    },
    "stripe": {
        "canonical_name": "Stripe, Inc.",
        "official_domain": "stripe.com",
        "career_url": "https://stripe.com/jobs",
        "allowed_hosts": ["stripe.com"],
        "ats_domains": ["boards.greenhouse.io/stripe"]
    },
    "airbnb": {
        "canonical_name": "Airbnb, Inc.",
        "official_domain": "airbnb.com",
        "career_url": "https://careers.airbnb.com",
        "allowed_hosts": ["airbnb.com", "careers.airbnb.com"],
        "ats_domains": []
    },
    "uber": {
        "canonical_name": "Uber Technologies, Inc.",
        "official_domain": "uber.com",
        "career_url": "https://www.uber.com/us/en/careers/",
        "allowed_hosts": ["uber.com", "www.uber.com"],
        "ats_domains": []
    },
    "infosys": {
        "canonical_name": "Infosys Limited",
        "official_domain": "infosys.com",
        "career_url": "https://career.infosys.com",
        "allowed_hosts": ["infosys.com", "career.infosys.com"],
        "ats_domains": []
    },
    "tcs": {
        "canonical_name": "Tata Consultancy Services",
        "official_domain": "tcs.com",
        "career_url": "https://www.tcs.com/careers",
        "allowed_hosts": ["tcs.com", "www.tcs.com", "ibegin.tcs.com"],
        "ats_domains": []
    },
    "wipro": {
        "canonical_name": "Wipro Limited",
        "official_domain": "wipro.com",
        "career_url": "https://careers.wipro.com",
        "allowed_hosts": ["wipro.com", "careers.wipro.com"],
        "ats_domains": []
    },
    "accenture": {
        "canonical_name": "Accenture plc",
        "official_domain": "accenture.com",
        "career_url": "https://www.accenture.com/careers",
        "allowed_hosts": ["accenture.com", "www.accenture.com"],
        "ats_domains": []
    },
    "deloitte": {
        "canonical_name": "Deloitte Touche Tohmatsu Limited",
        "official_domain": "deloitte.com",
        "career_url": "https://www.deloitte.com/careers",
        "allowed_hosts": ["deloitte.com", "www.deloitte.com", "jobs2.deloitte.com"],
        "ats_domains": []
    },
    "github": {
        "canonical_name": "GitHub, Inc.",
        "official_domain": "github.com",
        "career_url": "https://github.com/about/careers",
        "allowed_hosts": ["github.com"],
        "ats_domains": []
    }
}

# Recognized legitimate Applicant Tracking System (ATS) and job portal domains
TRUSTED_ATS_DOMAINS = [
    "greenhouse.io", "boards.greenhouse.io",
    "lever.co", "jobs.lever.co",
    "workday.com", "myworkdayjobs.com",
    "smartrecruiters.com",
    "ashbyhq.com", "jobs.ashbyhq.com",
    "icims.com",
    "taleo.net",
    "bamboohr.com",
    "breezy.hr",
    "jazzhr.com",
    "linkedin.com",
    "indeed.com"
]

# TLDs frequently used for throwaway phishing sites
SUSPICIOUS_TLDS = {".xyz", ".top", ".work", ".click", ".buzz", ".gq", ".ml", ".cf", ".tk", ".ga", ".fit", ".rest"}


def verify_company_and_domain(company_name: str, submitted_url: str = None) -> Dict[str, Any]:
    """
    Performs verified domain resolution, enterprise registry lookup,
    and checks whether the vacancy URL is corroborated by the official employer.
    """
    evidence: List[str] = []
    clean_company = (company_name or "").strip()
    normalized_key = re.sub(r"[^a-zA-Z0-9]", "", clean_company.lower())

    parsed_url = None
    url_domain = ""
    if submitted_url:
        try:
            parsed_url = urlparse(submitted_url)
            url_domain = (parsed_url.netloc or "").lower()
            if ":" in url_domain:
                url_domain = url_domain.split(":")[0]
        except Exception:
            pass

    # Check for suspicious top-level domains in submitted link
    if url_domain:
        for tld in SUSPICIOUS_TLDS:
            if url_domain.endswith(tld):
                evidence.append(f"Caution: Domain '{url_domain}' ends with high-risk TLD '{tld}'.")

    # Step 1: Check Known Enterprise Registry
    matched_entry = None
    for key, data in KNOWN_ENTERPRISE_REGISTRY.items():
        if key in normalized_key or normalized_key in key:
            matched_entry = data
            break

    if matched_entry:
        official_domain = matched_entry["official_domain"]
        career_url = matched_entry["career_url"]
        allowed_hosts = matched_entry["allowed_hosts"]
        ats_domains = matched_entry.get("ats_domains", [])

        evidence.append(f"Matched official enterprise profile: {matched_entry['canonical_name']} ({official_domain}).")

        # Check if submitted URL matches the official domain
        if url_domain:
            is_direct_match = any(url_domain == host or url_domain.endswith("." + host) for host in allowed_hosts)
            is_ats_match = any(ats in (submitted_url or "") for ats in ats_domains)
            is_trusted_ats = any(url_domain.endswith(ats) for ats in TRUSTED_ATS_DOMAINS)

            if is_direct_match or is_ats_match:
                evidence.append(f"Corroborated: Submitted URL is hosted directly on {matched_entry['canonical_name']}'s verified infrastructure.")
                return {
                    "status": "VERIFIED",
                    "claimed_company": matched_entry["canonical_name"],
                    "official_domain": official_domain,
                    "domain_verified": True,
                    "official_career_url": career_url,
                    "official_apply_url": submitted_url,
                    "vacancy_verified": True,
                    "evidence": evidence,
                    "notes": "Posting URL is corroborated on the verified corporate domain. Official apply option enabled."
                }
            elif is_trusted_ats:
                evidence.append(f"Submitted URL is hosted on trusted applicant portal ({url_domain}) for {matched_entry['canonical_name']}.")
                return {
                    "status": "VERIFIED",
                    "claimed_company": matched_entry["canonical_name"],
                    "official_domain": official_domain,
                    "domain_verified": True,
                    "official_career_url": career_url,
                    "official_apply_url": submitted_url,
                    "vacancy_verified": True,
                    "evidence": evidence,
                    "notes": "Posting verified on a recognized third-party recruitment platform. Official apply option enabled."
                }
            else:
                # Discrepancy detected! Claimed enterprise, but domain does NOT match
                evidence.append(
                    f"DOMAIN MISMATCH WARNING: The posting claims to be {matched_entry['canonical_name']} "
                    f"but is hosted on '{url_domain}', which is NOT an official domain ({official_domain})."
                )
                return {
                    "status": "MISMATCH",
                    "claimed_company": matched_entry["canonical_name"],
                    "official_domain": official_domain,
                    "domain_verified": False,
                    "official_career_url": career_url,
                    "official_apply_url": None,
                    "vacancy_verified": False,
                    "evidence": evidence,
                    "notes": f"Potential spoofing detected: Domain '{url_domain}' does not belong to {matched_entry['canonical_name']}."
                }
        else:
            # No URL provided; manual check for known company
            evidence.append(f"Official company career portal located: {career_url}")
            return {
                "status": "VERIFIED",
                "claimed_company": matched_entry["canonical_name"],
                "official_domain": official_domain,
                "domain_verified": True,
                "official_career_url": career_url,
                "official_apply_url": None,
                "vacancy_verified": False,
                "evidence": evidence,
                "notes": f"Company is verified in enterprise registry. Please inspect vacancy directly at {career_url}."
            }

    # Step 2: Arbitrary company domain discovery via DNS
    if clean_company:
        probable_domain = re.sub(r"[^a-zA-Z0-9-]", "", clean_company.lower().replace(" ", "")) + ".com"
        has_dns = False
        try:
            socket.gethostbyname(probable_domain)
            has_dns = True
        except Exception:
            pass

        if has_dns:
            evidence.append(f"Resolved public DNS records for '{probable_domain}'.")
            if url_domain and (url_domain == probable_domain or url_domain.endswith("." + probable_domain)):
                evidence.append(f"Submitted URL matches registered company domain '{probable_domain}'.")
                return {
                    "status": "VERIFIED",
                    "claimed_company": clean_company,
                    "official_domain": probable_domain,
                    "domain_verified": True,
                    "official_career_url": f"https://{probable_domain}",
                    "official_apply_url": submitted_url,
                    "vacancy_verified": True,
                    "evidence": evidence,
                    "notes": "Domain corroborated via authoritative DNS resolution."
                }
            elif url_domain and any(url_domain.endswith(ats) for ats in TRUSTED_ATS_DOMAINS):
                evidence.append(f"Posting hosted on trusted recruitment infrastructure ({url_domain}).")
                return {
                    "status": "VERIFIED",
                    "claimed_company": clean_company,
                    "official_domain": probable_domain,
                    "domain_verified": True,
                    "official_career_url": f"https://{probable_domain}",
                    "official_apply_url": submitted_url,
                    "vacancy_verified": True,
                    "evidence": evidence,
                    "notes": "Verified applicant tracking system link."
                }
            elif url_domain:
                evidence.append(f"Domain mismatch: Submitted on '{url_domain}', but company appears registered as '{probable_domain}'.")
                return {
                    "status": "UNVERIFIED",
                    "claimed_company": clean_company,
                    "official_domain": probable_domain,
                    "domain_verified": False,
                    "official_career_url": f"https://{probable_domain}",
                    "official_apply_url": None,
                    "vacancy_verified": False,
                    "evidence": evidence,
                    "notes": "Vacancy not verified on official domain. Exercise caution."
                }
            else:
                return {
                    "status": "INCONCLUSIVE",
                    "claimed_company": clean_company,
                    "official_domain": probable_domain,
                    "domain_verified": True,
                    "official_career_url": f"https://{probable_domain}",
                    "official_apply_url": None,
                    "vacancy_verified": False,
                    "evidence": evidence,
                    "notes": "Company domain exists, but vacancy URL was not provided for corroboration."
                }

    # Step 3: Inconclusive / Unregistered
    evidence.append("No authoritative official company records or DNS corroboration found.")
    return {
        "status": "INCONCLUSIVE",
        "claimed_company": clean_company or "Unknown",
        "official_domain": None,
        "domain_verified": False,
        "official_career_url": None,
        "official_apply_url": None,
        "vacancy_verified": False,
        "evidence": evidence,
        "notes": "Could not independently verify company domain or vacancy. Proceed with skepticism."
    }
