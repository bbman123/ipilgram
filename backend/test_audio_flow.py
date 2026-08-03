import httpx
import json

c = httpx.Client(timeout=60, follow_redirects=True)
base = "https://ipilgram.onrender.com/api/v1"

# Try seed user
r = c.post(f"{base}/auth/login", json={"email": "abdullah.ibrahim@example.com", "password": "pilgrim123"})
print(f"Login: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    token = data["access_token"]
    print(f"Token: {token[:40]}...")

    # Test /announcements/my
    r2 = c.get(f"{base}/announcements/my", headers={"Authorization": f"Bearer {token}"})
    print(f"Announcements: {r2.status_code}")
    if r2.status_code == 200:
        items = r2.json()
        print(f"Count: {len(items)}")
        for item in items:
            audio_url = item.get("audio_url", "")
            print(f"  title={item['title']!r} audio_url={audio_url!r}")
            if audio_url:
                if audio_url.startswith("http"):
                    full_url = audio_url
                else:
                    full_url = f"https://ipilgram.onrender.com{audio_url}"
                print(f"  Full URL: {full_url}")
                try:
                    r3 = c.get(full_url, timeout=30)
                    print(f"  Audio response: status={r3.status_code}, content-type={r3.headers.get('content-type','?')}, body_len={len(r3.content)}")
                    if r3.status_code != 200:
                        print(f"  Body: {r3.text[:300]}")
                except Exception as e:
                    print(f"  Audio request failed: {e}")
            else:
                print("  No audio_url")
    else:
        print(f"Error: {r2.text[:500]}")
else:
    print(f"Login failed: {r.text[:500]}")
