from app.services.scraper import is_safe_url
from app.services.rule_engine import rule_engine

def test_ssrf_blocks_localhost():
    is_safe, msg = is_safe_url("http://localhost:8000/internal")
    assert is_safe is False
    assert "localhost" in msg.lower() or "restricted" in msg.lower()

def test_ssrf_blocks_private_ip():
    is_safe, msg = is_safe_url("http://192.168.1.1/admin")
    assert is_safe is False
    assert "private" in msg.lower() or "restricted" in msg.lower()

def test_ssrf_blocks_loopback():
    is_safe, msg = is_safe_url("http://127.0.0.1:5000/secret")
    assert is_safe is False

def test_ssrf_blocks_unsupported_protocol():
    is_safe, msg = is_safe_url("file:///etc/passwd")
    assert is_safe is False
    assert "protocol" in msg.lower()

def test_rule_engine_detects_wire_and_telegram():
    res = rule_engine.evaluate(
        title="Payment Clerk",
        description="Must wire transfer money via Western Union. Text me on Telegram @scam_agent.",
        company="Fake Co"
    )
    assert res["rule_score"] >= 60.0
    signals = [s["name"] for s in res["signals"]]
    assert any("Telegram" in s for s in signals)
    assert any("Untraceable Payment" in s for s in signals)

def test_rule_engine_clean_job():
    res = rule_engine.evaluate(
        title="Staff Software Engineer",
        description="Design distributed microservices, write clean maintainable code, conduct peer reviews.",
        company="Datadog"
    )
    assert res["rule_score"] == 0.0
    assert len(res["signals"]) == 0
