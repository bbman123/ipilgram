import pytest


class TestPilgrims:
    def test_requires_admin(self, client):
        r = client.get("/api/v1/pilgrims")
        assert r.status_code == 401

    def test_list_pilgrims(self, client, admin_headers):
        r = client.get("/api/v1/pilgrims", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert "data" in body

    def test_list_with_pagination(self, client, admin_headers):
        r = client.get("/api/v1/pilgrims?page=1&size=5", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True

    def test_list_with_search(self, client, admin_headers):
        r = client.get("/api/v1/pilgrims?search=test", headers=admin_headers)
        assert r.status_code == 200


class TestFlights:
    def test_requires_admin(self, client):
        r = client.get("/api/v1/flights")
        assert r.status_code == 401

    def test_list_flights(self, client, admin_headers):
        r = client.get("/api/v1/flights", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True


class TestAccommodations:
    def test_requires_admin(self, client):
        r = client.get("/api/v1/accommodations")
        assert r.status_code == 401

    def test_list_accommodations(self, client, admin_headers):
        r = client.get("/api/v1/accommodations", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True


class TestTransports:
    def test_requires_admin(self, client):
        r = client.get("/api/v1/transports")
        assert r.status_code == 401

    def test_list_transports(self, client, admin_headers):
        r = client.get("/api/v1/transports", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True


class TestPackages:
    def test_requires_admin(self, client):
        r = client.get("/api/v1/packages")
        assert r.status_code == 401

    def test_list_packages(self, client, admin_headers):
        r = client.get("/api/v1/packages", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True


class TestAnnouncements:
    def test_requires_admin(self, client):
        r = client.get("/api/v1/announcements")
        assert r.status_code == 401

    def test_list_announcements(self, client, admin_headers):
        r = client.get("/api/v1/announcements", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True

    def test_active_announcements(self, client):
        r = client.get("/api/v1/announcements/active")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True

    def test_placeholders(self, client):
        r = client.get("/api/v1/announcements/templates/placeholders")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True


class TestPreferences:
    def test_requires_admin(self, client):
        r = client.get("/api/v1/preferences")
        assert r.status_code == 401

    def test_list_preferences(self, client, admin_headers):
        r = client.get("/api/v1/preferences", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True


class TestNotifications:
    def test_requires_admin(self, client):
        r = client.get("/api/v1/notifications")
        assert r.status_code == 401

    def test_list_notifications(self, client, admin_headers):
        r = client.get("/api/v1/notifications", headers=admin_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
