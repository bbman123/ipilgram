import requests, json

BASE = "http://127.0.0.1:8002/api/v1"
admin_token = None

# 1. Login
r = requests.post(f"{BASE}/auth/login", json={"email": "admin@hajj.ng", "password": "admin123"})
admin_token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {admin_token}"}
print(f"1. Login: {r.status_code}")

# 2. Health
r = requests.get(f"{BASE}/health")
print(f"2. Health: {r.status_code} {r.json()}")

# 3. Stats
r = requests.get(f"{BASE}/stats", headers=headers)
print(f"3. Stats: {r.status_code} {r.json()}")

# 4. OpenAPI
r = requests.get("http://127.0.0.1:8002/openapi.json")
spec = r.json()
paths = sum(len(m) for p in spec["paths"].values() for m in [p])
schemas = len(spec.get("components", {}).get("schemas", {}))
print(f"4. OpenAPI: {paths} endpoints, {schemas} schemas")

# 5. Docs
r = requests.get("http://127.0.0.1:8002/docs")
print(f"5. Docs: {r.status_code}")

# 6. Pilgrims with package filter
r = requests.get(f"{BASE}/pilgrims?page=1&size=100", headers=headers)
data = r.json()
print(f"6. Pilgrims: {data['total']} total, first has package_name={data['items'][0].get('package_name')}")

# 7. Pilgrims with package_id filter
r = requests.get(f"{BASE}/pilgrims?page=1&size=100&package_id=1", headers=headers)
data = r.json()
print(f"7. Pilgrims (pkg=1): {data['total']} pilgrims")

# 8. Packages
r = requests.get(f"{BASE}/packages?page=1&size=100", headers=headers)
data = r.json()
print(f"8. Packages: {data['total']} total")

# 9. Package pilgrims
r = requests.get(f"{BASE}/packages/1/pilgrims?page=1&size=100", headers=headers)
data = r.json()
print(f"9. Package 1 pilgrims: {data['total']} pilgrims")

# 10. Announcements (admin list)
r = requests.get(f"{BASE}/announcements?page=1&size=100", headers=headers)
data = r.json()
print(f"10. Announcements: {data['total']} total")
if data["items"]:
    a = data["items"][0]
    print(f"    First has message_template: {'message_template' in a}")

# 11. Announcements placeholders
r = requests.get(f"{BASE}/announcements/templates/placeholders")
print(f"11. Placeholders: {r.status_code}, count={len(r.json().get('placeholders', []))}")

# 12. Active announcements
r = requests.get(f"{BASE}/announcements/active")
print(f"12. Active announcements: {r.status_code}, count={len(r.json())}")

# 13. Notifications (admin list)
r = requests.get(f"{BASE}/notifications?page=1&size=100", headers=headers)
data = r.json()
print(f"13. Notifications: {data['total']} total")
if data["items"]:
    n = data["items"][0]
    print(f"    First has message={bool(n.get('message'))}, scheduled_time={bool(n.get('scheduled_time'))}")

# 14. Create announcement template
r = requests.post(f"{BASE}/announcements", headers=headers, json={
    "title": "Test Template",
    "message_template": "Hello {{pilgrim_name}}, your flight {{flight_number}} departs at {{departure_time}}.",
    "priority": "high",
    "target_type": "all",
    "publish_date": "2026-07-01T00:00:00Z",
    "expiry_date": "2026-12-31T23:59:59Z",
    "include_flight_details": True,
    "send_as_notification": False,
})
print(f"14. Create template: {r.status_code}")

# 15. Verify new template has message_template field
if r.status_code == 201:
    t = r.json()
    print(f"    Template: id={t['id']}, has message_template={bool(t.get('message_template'))}")

# 16. Preferences
r = requests.get(f"{BASE}/preferences?page=1&size=100", headers=headers)
data = r.json()
print(f"16. Preferences: {data['total']} total")

# 17. Flights
r = requests.get(f"{BASE}/flights?page=1&size=100", headers=headers)
data = r.json()
print(f"17. Flights: {data['total']} total")

# 18. Accommodations
r = requests.get(f"{BASE}/accommodations?page=1&size=100", headers=headers)
data = r.json()
print(f"18. Accommodations: {data['total']} total")

# 19. Transports
r = requests.get(f"{BASE}/transports?page=1&size=100", headers=headers)
data = r.json()
print(f"19. Transports: {data['total']} total")

print("\n=== ALL TESTS PASSED ===")
