import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault("DATABASE_URL", "postgresql://postgres:nerdyamin@localhost:5432/hajj_pilgrims")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only-32chars!")
os.environ.setdefault("DEBUG", "true")

from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture(scope="session")
def admin_headers(client):
    r = client.post("/api/v1/auth/login", json={"email": "admin@hajj.ng", "password": "admin123"})
    if r.status_code != 200:
        pytest.skip(f"Admin login failed: {r.status_code} {r.json()}")
    body = r.json()
    token = body.get("access_token") or body.get("data", {}).get("access_token")
    if not token:
        pytest.skip(f"No access_token in response: {body}")
    return {"Authorization": f"Bearer {token}"}
