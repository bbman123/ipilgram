"""End-to-end trace of the multilingual announcement pipeline.

Logs in as admin, reads DB state via API, then logs in as pilgrim
and traces GET /announcements/my through every variable.
"""

import httpx
import json
import sys

BASE = "https://ipilgram.onrender.com/api/v1"


def main():
    # ── STEP 1: Login as admin ──────────────────────────────────────────
    print("=" * 70)
    print("STEP 1: LOGIN AS ADMIN")
    print("=" * 70)
    r = httpx.post(f"{BASE}/auth/login", json={"email": "admin@hajj.ng", "password": "admin123"}, timeout=30)
    assert r.status_code == 200, f"Admin login failed: {r.status_code} {r.text}"
    admin_token = r.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print(f"  admin_token = {admin_token[:30]}...")
    print()

    # ── STEP 2: All preferences ─────────────────────────────────────────
    print("=" * 70)
    print("STEP 2: ALL PREFERENCES IN DATABASE")
    print("=" * 70)
    r = httpx.get(f"{BASE}/preferences?page=1&size=100", headers=admin_headers, timeout=30)
    print(f"  HTTP {r.status_code}")
    data = r.json()
    if r.status_code != 200:
        print(f"  ERROR: {json.dumps(data, indent=2)[:500]}")
        print()
    else:
        total = data.get("total", "N/A")
        items = data.get("items", [])
        if not items and isinstance(data.get("data"), dict):
            items = data["data"].get("items", [])
            total = data["data"].get("total", total)
        print(f"  Total preferences: {total}")
        for item in items:
            lang = item.get("preferred_language", "N/A")
            print(f"  Preference ID={item.get('id')}, pilgrim_id={item.get('pilgrim_id')}, "
                  f"pilgrim_name={item.get('pilgrim_name')}, "
                  f"preferred_language={lang}, "
                  f"type={type(lang).__name__}, "
                  f"delivery_mode={item.get('delivery_mode')}")
        if not items:
            print("  *** NO PREFERENCES FOUND IN DATABASE ***")
    print()

    # ── STEP 3: All pilgrims ────────────────────────────────────────────
    print("=" * 70)
    print("STEP 3: ALL PILGRIMS")
    print("=" * 70)
    r = httpx.get(f"{BASE}/pilgrims?page=1&size=100", headers=admin_headers, timeout=30)
    print(f"  HTTP {r.status_code}")
    data = r.json()
    total = data.get("total", "N/A")
    items = data.get("items", [])
    if not items and isinstance(data.get("data"), dict):
        items = data["data"].get("items", [])
        total = data["data"].get("total", total)
    print(f"  Total pilgrims: {total}")
    for item in items:
        print(f"  Pilgrim ID={item.get('id')}, name={item.get('full_name')}, "
              f"email={item.get('email')}, package_id={item.get('package_id')}")
    print()

    # ── STEP 4: All announcements ───────────────────────────────────────
    print("=" * 70)
    print("STEP 4: ALL ANNOUNCEMENTS")
    print("=" * 70)
    r = httpx.get(f"{BASE}/announcements?page=1&size=100", headers=admin_headers, timeout=30)
    print(f"  HTTP {r.status_code}")
    data = r.json()
    total = data.get("total", "N/A")
    items = data.get("items", [])
    if not items and isinstance(data.get("data"), dict):
        items = data["data"].get("items", [])
        total = data["data"].get("total", total)
    print(f"  Total announcements: {total}")
    for item in items:
        print(f"  Announcement ID={item.get('id')}")
        print(f"    title          = {item.get('title')}")
        msg = item.get("message_template", "")
        print(f"    message_template = {msg[:120]}{'...' if len(str(msg)) > 120 else ''}")
        print(f"    priority       = {item.get('priority')}")
        print(f"    target_type    = {item.get('target_type')}")
        print(f"    target_id      = {item.get('target_id')}")
        print(f"    publish_date   = {item.get('publish_date')}")
        print(f"    expiry_date    = {item.get('expiry_date')}")
    print()

    # ── STEP 5: Find an Arabic-speaking pilgrim ──────────────────────────
    print("=" * 70)
    print("STEP 5: IDENTIFY ARABIC-SPEAKING PILGRIM")
    print("=" * 70)
    arabic_pilgrim_id = None
    for item in items:
        pass  # just iterate announcements above
    # Re-read preferences
    r = httpx.get(f"{BASE}/preferences?page=1&size=100", headers=admin_headers, timeout=30)
    pref_data = r.json()
    pref_items = pref_data.get("items", [])
    if not pref_items and isinstance(pref_data.get("data"), dict):
        pref_items = pref_data["data"].get("items", [])

    arabic_pref = None
    for pref in pref_items:
        lang = pref.get("preferred_language", "")
        print(f"  Checking preference: pilgrim_id={pref.get('pilgrim_id')}, language={lang}")
        if lang == "Arabic":
            arabic_pref = pref
            arabic_pilgrim_id = pref.get("pilgrim_id")
            print(f"  >>> FOUND ARABIC PREFERENCE: pilgrim_id={arabic_pilgrim_id}")
            break

    if not arabic_pilgrim_id:
        print("  *** NO ARABIC PREFERENCE FOUND ***")
        print("  Selecting first available pilgrim to demonstrate the pipeline...")
        r = httpx.get(f"{BASE}/pilgrims?page=1&size=100", headers=admin_headers, timeout=30)
        pil_data = r.json()
        pil_items = pil_data.get("items", [])
        if not pil_items and isinstance(pil_data.get("data"), dict):
            pil_items = pil_data["data"].get("items", [])
        if pil_items:
            arabic_pilgrim_id = pil_items[0].get("id")
            print(f"  Using pilgrim_id={arabic_pilgrim_id} (no Arabic preference set)")
        else:
            print("  *** NO PILGRIMS IN DATABASE. Cannot trace. ***")
            return
    print()

    # ── STEP 6: Login as the pilgrim ────────────────────────────────────
    print("=" * 70)
    print(f"STEP 6: LOGIN AS PILGRIM (id={arabic_pilgrim_id})")
    print("=" * 70)
    r = httpx.get(f"{BASE}/pilgrims?page=1&size=100", headers=admin_headers, timeout=30)
    pil_data = r.json()
    pil_items = pil_data.get("items", [])
    if not pil_items and isinstance(pil_data.get("data"), dict):
        pil_items = pil_data["data"].get("items", [])

    pilgrim_email = None
    pilgrim_name = None
    for p in pil_items:
        if p.get("id") == arabic_pilgrim_id:
            pilgrim_email = p.get("email")
            pilgrim_name = p.get("full_name")
            break

    if not pilgrim_email:
        print(f"  *** Cannot find email for pilgrim_id={arabic_pilgrim_id} ***")
        return

    print(f"  pilgrim_name  = {pilgrim_name}")
    print(f"  pilgrim_email = {pilgrim_email}")

    r = httpx.post(f"{BASE}/auth/login", json={"email": pilgrim_email, "password": "pilgrim123"}, timeout=30)
    if r.status_code != 200:
        print(f"  *** Login failed: {r.status_code} {r.text[:200]} ***")
        print("  Trying password 'password123'...")
        r = httpx.post(f"{BASE}/auth/login", json={"email": pilgrim_email, "password": "password123"}, timeout=30)
    if r.status_code != 200:
        print(f"  *** Login still failed: {r.status_code} ***")
        return

    pilgrim_token = r.json()["access_token"]
    pilgrim_headers = {"Authorization": f"Bearer {pilgrim_token}"}
    print(f"  pilgrim_token = {pilgrim_token[:30]}...")
    print()

    # ── STEP 7: GET /announcements/my (FULL TRACE) ──────────────────────
    print("=" * 70)
    print("STEP 7: GET /announcements/my — FULL PIPELINE TRACE")
    print("=" * 70)
    r = httpx.get(f"{BASE}/announcements/my", headers=pilgrim_headers, timeout=60)
    print(f"  HTTP {r.status_code}")
    resp_data = r.json()
    if r.status_code != 200:
        print(f"  ERROR RESPONSE: {json.dumps(resp_data, indent=2)[:1000]}")
        print()
        print("  *** CANNOT CONTINUE TRACE — endpoint returned error ***")
        return
    announcements = resp_data.get("data", [])
    if not announcements and isinstance(resp_data, list):
        announcements = resp_data
    print(f"  Number of announcements returned: {len(announcements)}")
    print()

    for idx, ann in enumerate(announcements):
        print(f"  --- Announcement {idx + 1} ---")
        print(f"    id           = {ann.get('id')}")
        print(f"    title        = {ann.get('title')}")
        print(f"    message      = {ann.get('message')}")
        print(f"    priority     = {ann.get('priority')}")
        print(f"    simplified   = {ann.get('simplified')}")
        print(f"    translated   = {ann.get('translated')}")
        print(f"    language     = {ann.get('language')}")
        print(f"    audio_url    = {ann.get('audio_url')}")
        print(f"    publish_date = {ann.get('publish_date')}")
        print(f"    expiry_date  = {ann.get('expiry_date')}")
        print()

        # ── STEP 8: Flutter receives this exact JSON ────────────────────
        print(f"    STEP 8: FLUTTER DESERIALIZES INTO PersonalizedAnnouncement")
        print(f"      .id           = {ann.get('id')} (int)")
        print(f"      .title        = \"{ann.get('title')}\" (String)")
        msg = ann.get('message', '')
        print(f"      .message      = \"{msg[:80]}{'...' if len(msg) > 80 else ''}\" (String)")
        print(f"      .translated   = {ann.get('translated')} (bool)")
        print(f"      .language     = \"{ann.get('language')}\" (String)")
        print(f"      .audio_url    = \"{ann.get('audio_url')}\" (String?)")
        print()

        # ── STEP 9: Audio trace ─────────────────────────────────────────
        audio_url = ann.get("audio_url")
        if audio_url:
            print(f"    STEP 9: AUDIO CENTER RECEIVES audio_url = \"{audio_url}\"")
            full_url = audio_url if audio_url.startswith("http") else f"https://ipilgram.onrender.com{audio_url}"
            print(f"    Full audio URL = \"{full_url}\"")

            # Try to HEAD the audio file
            try:
                hr = httpx.head(full_url, timeout=15, follow_redirects=True)
                print(f"    HEAD status    = {hr.status_code}")
                print(f"    Content-Type   = {hr.headers.get('content-type', 'N/A')}")
                print(f"    Content-Length  = {hr.headers.get('content-length', 'N/A')} bytes")
            except Exception as e:
                print(f"    HEAD failed    = {e}")
        else:
            print(f"    STEP 9: audio_url is NULL — no audio generated")
        print()

    # ── SUMMARY ─────────────────────────────────────────────────────────
    print("=" * 70)
    print("TRACE SUMMARY")
    print("=" * 70)
    print(f"  Pilgrim ID       = {arabic_pilgrim_id}")
    print(f"  Pilgrim name     = {pilgrim_name}")
    print(f"  Preference found = {arabic_pref is not None}")
    if arabic_pref:
        print(f"  Preferred lang   = {arabic_pref.get('preferred_language')}")
    else:
        print(f"  Preferred lang   = NONE (no preference record)")
    print(f"  Announcements    = {len(announcements)}")
    for ann in announcements:
        print(f"    [{ann.get('id')}] translated={ann.get('translated')}, "
              f"language={ann.get('language')}, "
              f"audio={'YES' if ann.get('audio_url') else 'NO'}")
    print()


if __name__ == "__main__":
    main()
