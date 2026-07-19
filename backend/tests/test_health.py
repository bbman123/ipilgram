import pytest


class TestHealth:
    def test_health(self, client):
        r = client.get("/api/v1/health")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert "data" in body

    def test_health_has_status(self, client):
        r = client.get("/api/v1/health")
        data = r.json()["data"]
        assert "status" in data


class TestStats:
    def test_stats_requires_admin(self, client):
        r = client.get("/api/v1/stats")
        assert r.status_code == 401

    def test_stats_ok(self, client, admin_headers):
        r = client.get("/api/v1/stats", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert "data" in body
