"""Probe every endpoint to find exact break point."""

import httpx
import json

BASE = "https://ipilgram.onrender.com/api/v1"

r = httpx.post(f"{BASE}/auth/login", json={"email": "admin@hajj.ng", "password": "admin123"}, timeout=30)
token = r.json()["access_token"]
h = {"Authorization": f"Bearer {token}"}

endpoints = [
    "/pilgrims?page=1&size=5",
    "/announcements?page=1&size=5",
    "/flights?page=1&size=5",
    "/accommodations?page=1&size=5",
    "/transports?page=1&size=5",
    "/packages?page=1&size=5",
    "/notifications?page=1&size=5",
    "/preferences?page=1&size=5",
    "/preferences/by-pilgrim/8",
    "/stats",
]

print("ENDPOINT HEALTH MAP")
print("=" * 70)
for ep in endpoints:
    try:
        r = httpx.get(f"{BASE}{ep}", headers=h, timeout=30)
        status = r.status_code
        symbol = "OK" if status == 200 else "FAIL"
        msg = ""
        if status != 200:
            try:
                msg = r.json().get("message", "")[:80]
            except Exception:
                msg = r.text[:80]
        print(f"  [{symbol}] {ep:40s} HTTP {status}  {msg}")
    except Exception as e:
        print(f"  [ERR] {ep:40s} {e}")

# Now try announcements/my as a pilgrim (not admin)
print()
print("ANNOUNCEMENTS/MY AS PILGRIM")
print("=" * 70)
r = httpx.post(f"{BASE}/auth/login", json={"email": "zainab.abubakar@example.com", "password": "pilgrim123"}, timeout=30)
if r.status_code == 200:
    pt = r.json()["access_token"]
    ph = {"Authorization": f"Bearer {pt}"}
    r = httpx.get(f"{BASE}/announcements/my", headers=ph, timeout=60)
    print(f"  HTTP {r.status_code}")
    if r.status_code != 200:
        print(f"  Response: {json.dumps(r.json(), indent=2)[:800]}")
    else:
        items = r.json().get("data", [])
        print(f"  Got {len(items)} announcements")
else:
    print(f"  Login failed: {r.status_code}")

# Check the AI chat endpoint too
print()
print("AI CHAT /ask")
print("=" * 70)
r = httpx.post(f"{BASE}/auth/login", json={"email": "zainab.abubakar@example.com", "password": "pilgrim123"}, timeout=30)
if r.status_code == 200:
    pt = r.json()["access_token"]
    ph = {"Authorization": f"Bearer {pt}", "Content-Type": "application/json"}
    r = httpx.post(f"{BASE}/personalize/ask", headers=ph, json={"query": "When is my flight?"}, timeout=60)
    print(f"  HTTP {r.status_code}")
    if r.status_code != 200:
        print(f"  Response: {json.dumps(r.json(), indent=2)[:800]}")
    else:
        data = r.json().get("data", r.json())
        print(f"  Response: {json.dumps(data, indent=2)[:500]}")
