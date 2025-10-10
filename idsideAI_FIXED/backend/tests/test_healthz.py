from app import app
from fastapi.testclient import TestClient

def test_healthz_ok():
    c = TestClient(app)
    r = c.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
