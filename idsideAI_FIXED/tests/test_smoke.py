from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_billing_plans():
    r = client.get("/billing/plans")
    assert r.status_code == 200
    assert "plans" in r.json()
