# Fake Job Detection & Verification Platform - REST API Reference

The backend exposes a REST API powered by FastAPI. Interactive documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc).

Base URL: `http://localhost:8000/api`

---

## 1. System Health

### `GET /api/health`
Returns operational telemetry, environment, and model loading status.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "app_name": "Fake Job Detection & Verification Platform",
  "version": "1.0.0",
  "environment": "development",
  "ml_model_loaded": true,
  "dataset_available": true,
  "database": "connected"
}
```

---

## 2. Job Threat Analysis

### `POST /api/analyze`
Submits a job advertisement for forensic threat scanning and official domain corroboration.

**Request Body:**
```json
{
  "job_title": "Senior Cloud Backend Engineer",
  "company_name": "Google",
  "job_description": "We are seeking a senior engineer to build distributed systems in Python and Go.",
  "job_url": "https://careers.google.com/jobs/results/12345"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "timestamp": "2026-10-14T09:20:00Z",
  "job_title": "Senior Cloud Backend Engineer",
  "company_name": "Google",
  "job_url": "https://careers.google.com/jobs/results/12345",
  "job_description_snippet": "We are seeking a senior engineer...",
  "classification": "SAFE",
  "risk_score": 12.5,
  "risk_level_explanation": "Low threat probability. Standard corporate hiring language observed.",
  "ml_prediction": {
    "is_fake": false,
    "confidence": 0.94,
    "fraud_probability": 0.06,
    "features_analyzed": ["job_title", "company_profile", "description", "requirements"],
    "is_fallback": false,
    "algorithm": "TF-IDF + Calibrated Logistic Regression (EMSCAD trained)"
  },
  "detected_signals": [],
  "verification": {
    "status": "VERIFIED",
    "claimed_company": "Google LLC",
    "official_domain": "google.com",
    "domain_verified": true,
    "official_career_url": "https://careers.google.com",
    "official_apply_url": "https://careers.google.com/jobs/results/12345",
    "vacancy_verified": true,
    "evidence": ["Matched official enterprise profile: Google LLC (google.com)."],
    "notes": "Posting URL is corroborated on the verified corporate domain. Official apply option enabled."
  },
  "recommendations": [
    "This job posting displays standard legitimate characteristics.",
    "Always apply directly through the employer's official careers portal whenever available."
  ],
  "disclaimer": "Notice: While this system uses machine learning... a low-risk score does not guarantee employment authenticity."
}
```

---

## 3. URL Extraction

### `POST /api/extract`
Safely retrieves title, company, and description from a job URL with SSRF protection.

**Request Body:**
```json
{
  "url": "https://careers.google.com/jobs/results/12345"
}
```

---

## 4. Employer Domain Verification

### `POST /api/verify`
Independently verifies company registration, official careers URL, and corroboration status.

**Request Body:**
```json
{
  "company_name": "Microsoft",
  "job_url": "https://careers.microsoft.com"
}
```

---

## 5. Job Search & Feed

### `GET /api/jobs/search?q={query}&classification={SAFE|SUSPICIOUS|HIGH_RISK}&limit=12&offset=0`
Searches cataloged job postings with verified links or identified fraud signatures.

### `GET /api/jobs/dashboard/stats`
Returns aggregated analytics: total scans, safe count, suspicious count, high-risk count, and recent checks.

---

## 6. Audit History

### `GET /api/history?q={query}&classification={filter}&limit=20&offset=0`
Retrieves chronological audit logs stored in the database.

### `GET /api/history/{id}`
Retrieves full report details for a specific scan ID.

### `DELETE /api/history/{id}`
Deletes an audit record by ID.
