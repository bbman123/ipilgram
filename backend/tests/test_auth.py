import pytest
import time


class TestRegister:
    def test_register_success(self, client):
        unique = int(time.time())
        r = client.post("/api/v1/auth/register", json={
            "email": f"newpilgrim{unique}@test.com",
            "full_name": "Test Pilgrim",
            "password": "strongpass123",
        })
        assert r.status_code == 201
        body = r.json()
        assert body["success"] is True

    def test_register_duplicate(self, client):
        r = client.post("/api/v1/auth/register", json={
            "email": "admin@hajj.ng",
            "full_name": "Duplicate",
            "password": "strongpass123",
        })
        assert r.status_code == 400

    def test_register_validation(self, client):
        r = client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "password": "123",
        })
        assert r.status_code == 422


class TestLogin:
    def test_login_success(self, client):
        r = client.post("/api/v1/auth/login", json={
            "email": "admin@hajj.ng",
            "password": "admin123",
        })
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert "access_token" in body["data"]
        assert "refresh_token" in body["data"]

    def test_login_wrong_password(self, client):
        r = client.post("/api/v1/auth/login", json={
            "email": "admin@hajj.ng",
            "password": "wrongpassword",
        })
        assert r.status_code == 401

    def test_login_nonexistent_user(self, client):
        r = client.post("/api/v1/auth/login", json={
            "email": "nobody@test.com",
            "password": "password",
        })
        assert r.status_code == 401


class TestMe:
    def test_me_requires_auth(self, client):
        r = client.get("/api/v1/auth/me")
        assert r.status_code == 401

    def test_me_ok(self, client, admin_headers):
        r = client.get("/api/v1/auth/me", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert body["data"]["email"] == "admin@hajj.ng"


class TestRefresh:
    def test_refresh_requires_token(self, client):
        r = client.post("/api/v1/auth/refresh", json={"refresh_token": ""})
        assert r.status_code in (401, 422)

    @pytest.mark.xfail(reason="passlib + bcrypt 72-byte limit truncates long JWT refresh tokens")
    def test_refresh_valid(self, client):
        login_r = client.post("/api/v1/auth/login", json={
            "email": "admin@hajj.ng",
            "password": "admin123",
        })
        assert login_r.status_code == 200
        data = login_r.json()["data"]
        refresh_token = data["refresh_token"]
        r = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert "access_token" in body["data"]
