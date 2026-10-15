def test_verify_enterprise_matching_url(client):
    response = client.post("/api/verify", json={
        "company_name": "Google",
        "job_url": "https://careers.google.com/jobs/results/98765"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "VERIFIED"
    assert data["domain_verified"] is True
    assert data["vacancy_verified"] is True
    assert data["official_domain"] == "google.com"

def test_verify_enterprise_domain_mismatch(client):
    response = client.post("/api/verify", json={
        "company_name": "Amazon",
        "job_url": "https://amazon-recruiter-hub.xyz/jobs"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "MISMATCH"
    assert data["vacancy_verified"] is False
    assert data["official_apply_url"] is None
