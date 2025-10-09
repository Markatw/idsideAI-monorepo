# idsideAI_FIXED/tests/test_healthz.py
from fastapi.testclient import TestClient
from idsideai.main import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert "ok" in r.text.lower()
