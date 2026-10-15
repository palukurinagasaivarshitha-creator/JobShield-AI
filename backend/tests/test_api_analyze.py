def test_analyze_legitimate_job(client):
    payload = {
        "job_title": "Senior Python Backend Engineer",
        "company_name": "Google",
        "job_description": "We are seeking a senior engineer to build distributed systems in Python, Go, and Kubernetes. Requires a Bachelor's degree and 5 years experience.",
        "job_url": "https://careers.google.com/jobs/results/12345"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] in ("SAFE", "SUSPICIOUS")
    assert data["risk_score"] < 50.0
    assert "ml_prediction" in data
    assert "verification" in data
    assert data["verification"]["status"] == "VERIFIED"
    assert data["verification"]["vacancy_verified"] is True
    assert data["verification"]["official_apply_url"] == payload["job_url"]

def test_analyze_fraudulent_scam_job(client):
    payload = {
        "job_title": "Data Entry Remote Assistant",
        "company_name": "Quick Cash Ltd",
        "job_description": "Immediate start without interview! Earn $5000/week from home. Candidates must pay a $150 registration fee via Western Union or Bitcoin. Reach out on Telegram @quick_pay_hr.",
        "job_url": None
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "HIGH_RISK"
    assert data["risk_score"] >= 70.0
    assert len(data["detected_signals"]) >= 2
    # Verify fee and telegram signals detected
    signal_names = [s["name"] for s in data["detected_signals"]]
    assert any("Registration" in s or "Fee" in s for s in signal_names)
    assert any("Telegram" in s for s in signal_names)

def test_analyze_domain_mismatch_phishing(client):
    payload = {
        "job_title": "Executive Assistant",
        "company_name": "Microsoft",
        "job_description": "Join Microsoft remote operations. Apply on our private job board.",
        "job_url": "https://microsoft-career-portal.xyz/apply"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verification"]["status"] == "MISMATCH"
    assert data["verification"]["vacancy_verified"] is False
    assert data["verification"]["official_apply_url"] is None
    assert data["risk_score"] >= 40.0

def test_analyze_empty_request_validation(client):
    payload = {
        "job_title": "Developer",
        "company_name": "Test Co",
        "job_description": "",
        "job_url": ""
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422  # Pydantic validation error
