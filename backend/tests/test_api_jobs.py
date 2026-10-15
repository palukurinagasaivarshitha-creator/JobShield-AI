def test_search_jobs(client):
    response = client.get("/api/jobs/search?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check fields in first result
    first = data[0]
    assert "title" in first
    assert "company" in first
    assert "is_verified_posting" in first

def test_search_jobs_with_query(client):
    response = client.get("/api/jobs/search?q=Google")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("Google" in item["company"] for item in data)

def test_dashboard_stats(client):
    response = client.get("/api/jobs/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_scans" in data
    assert "safe_count" in data
    assert "suspicious_count" in data
    assert "high_risk_count" in data
    assert "recent_checks" in data
