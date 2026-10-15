import ipaddress
import json
import logging
import re
import socket
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
from app.core.config import settings

logger = logging.getLogger(__name__)

# Private / reserved network blocks for SSRF protection
BLOCKED_IP_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),      # Cloud metadata (AWS/GCP/Azure)
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]

def is_safe_url(url: str) -> tuple[bool, str]:
    """
    Validates URL scheme, resolves hostname, and checks against private/internal IP ranges (SSRF mitigation).
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False, f"Unsupported URL protocol: '{parsed.scheme}'. Only http and https are permitted."
        
        hostname = parsed.hostname
        if not hostname:
            return False, "Invalid URL: missing valid hostname."
        
        # Check against common local hostnames
        if hostname.lower() in ("localhost", "127.0.0.1", "0.0.0.0", "metadata.google.internal", "instance-data"):
            return False, "Access to localhost and internal cloud metadata addresses is forbidden."

        # Resolve IP addresses for hostname
        try:
            addr_info = socket.getaddrinfo(hostname, None)
        except socket.gaierror:
            return False, f"Could not resolve domain name: '{hostname}'"

        for item in addr_info:
            ip_str = item[4][0]
            ip_obj = ipaddress.ip_address(ip_str)
            for blocked_net in BLOCKED_IP_NETWORKS:
                if ip_obj in blocked_net:
                    return False, f"SSRF Guard: Resolved IP {ip_str} belongs to a private or restricted network."

        return True, ""
    except Exception as e:
        return False, f"URL validation error: {str(e)}"


def extract_job_from_url(url: str) -> dict:
    """
    Safely fetches and parses job information from an external web page.
    Implements size limits, timeouts, and safe DOM traversal.
    """
    is_safe, error_msg = is_safe_url(url)
    if not is_safe:
        raise ValueError(error_msg)

    headers = {
        "User-Agent": settings.USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        with httpx.Client(timeout=settings.REQUEST_TIMEOUT_SECONDS, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            
            # Check content length header
            content_length = response.headers.get("content-length")
            if content_length and int(content_length) > settings.MAX_CONTENT_LENGTH_BYTES:
                raise ValueError("Target webpage exceeds maximum allowed size (2MB).")

            response.raise_for_status()

            # Prevent reading overly large payload
            content = response.content
            if len(content) > settings.MAX_CONTENT_LENGTH_BYTES:
                raise ValueError("Target webpage response content exceeds safety limit.")

    except httpx.HTTPStatusError as e:
        raise ValueError(f"Server responded with error status {e.response.status_code}")
    except httpx.TimeoutException:
        raise ValueError("Connection timed out while attempting to reach the job posting URL.")
    except httpx.RequestError as e:
        raise ValueError(f"Failed to fetch job posting URL: {str(e)}")

    # Parse HTML safely
    soup = BeautifulSoup(content, "html.parser")

    # Remove script, style, navigation and footer tags to avoid false textual signals
    for tag in soup(["script", "style", "noscript", "svg", "header", "footer", "nav"]):
        tag.decompose()

    meta_tags = {}
    title = ""
    company = ""
    description = ""

    # Check for Schema.org JobPosting in JSON-LD
    for script_tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script_tag.string)
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "JobPosting":
                        data = item
                        break
            if isinstance(data, dict) and data.get("@type") == "JobPosting":
                title = data.get("title", "")
                hiring_org = data.get("hiringOrganization")
                if isinstance(hiring_org, dict):
                    company = hiring_org.get("name", "")
                elif isinstance(hiring_org, str):
                    company = hiring_org
                description = data.get("description", "")
                break
        except Exception:
            pass

    # OpenGraph Fallback
    og_title = soup.find("meta", property="og:title") or soup.find("meta", attrs={"name": "twitter:title"})
    if og_title and not title:
        title = og_title.get("content", "").strip()

    og_site_name = soup.find("meta", property="og:site_name")
    if og_site_name and not company:
        company = og_site_name.get("content", "").strip()

    og_desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
    if og_desc and not description:
        description = og_desc.get("content", "").strip()

    # Title fallback from <title> or <h1>
    if not title:
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            title = title_tag.string.strip()
        elif soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)

    # Clean description from body text if still empty
    if not description:
        main_content = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile(r"job|description|posting|career", re.I))
        if main_content:
            description = main_content.get_text(separator="\n", strip=True)
        else:
            description = soup.get_text(separator="\n", strip=True)

    # Heuristic company extraction if still missing
    if not company:
        # Check title patterns like "Software Engineer at Acme Corp" or "Acme Corp - Senior Developer"
        match = re.search(r"\bat\s+([A-Z][A-Za-z0-9\s&.,]{2,30})", title)
        if match:
            company = match.group(1).strip()
        else:
            parts = re.split(r"[-|–—:]", title)
            if len(parts) > 1 and len(parts[-1].strip()) < 40:
                company = parts[-1].strip()

    parsed_url = urlparse(url)
    source_domain = parsed_url.netloc.lower()

    return {
        "title": title[:200] if title else "Extracted Job Posting",
        "company": company[:150] if company else "Unspecified Employer",
        "description": description[:10000] if description else "No textual description could be extracted.",
        "canonical_url": url,
        "source_domain": source_domain,
    }
