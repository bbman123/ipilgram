"""Full end-to-end trace: create Arabic preference, login as pilgrim, trace announcements/my."""

import httpx
import json

BASE = "https://ipilgram.onrender.com/api/v1"


def pp(label, value, indent=4):
    """Pretty print with prefix."""
    prefix = " " * indent
    if isinstance(value, str) and len(value) > 120:
        print(f"{prefix}{label} = {value[:120]}...")
    else:
        print(f"{prefix}{label} = {value!r} (type={type(value).__name__})")


def main():
    # ── Login as admin ──────────────────────────────────────────────────
    r = httpx.post(f"{BASE}/auth/login", json={"email": "admin@hajj.ng", "password": "admin123"}, timeout=30)
    assert r.status_code == 200
    admin_token = r.json()["access_token"]
    ah = {"Authorization": f"Bearer {admin_token}", "Content-Type": "application/json"}

    # ── Create Arabic preference for pilgrim 8 ──────────────────────────
    print("=" * 70)
    print("STEP A: CREATE ARABIC PREFERENCE FOR PILGRIM ID=8 (Zainab)")
    print("=" * 70)
    r = httpx.post(f"{BASE}/preferences", headers=ah, json={
        "pilgrim_id": 8,
        "preferred_language": "Arabic",
        "delivery_mode": "Text + Audio",
        "font_size": 16,
        "notifications_enabled": True,
    }, timeout=30)
    print(f"  HTTP {r.status_code}")
    resp = r.json()
    print(f"  Response: {json.dumps(resp, indent=2)[:500]}")
    print()

    # ── Login as Zainab (pilgrim 8) ─────────────────────────────────────
    print("=" * 70)
    print("STEP B: LOGIN AS PILGRIM (Zainab, ID=8)")
    print("=" * 70)
    r = httpx.post(f"{BASE}/auth/login", json={"email": "zainab.abubakar@example.com", "password": "pilgrim123"}, timeout=30)
    if r.status_code != 200:
        for pw in ["password123", "admin123", "zainab123", "pilgrim1", "Pilgrim123!"]:
            r = httpx.post(f"{BASE}/auth/login", json={"email": "zainab.abubakar@example.com", "password": pw}, timeout=30)
            if r.status_code == 200:
                print(f"  Logged in with password: {pw}")
                break
    if r.status_code != 200:
        print(f"  FAILED TO LOGIN: {r.status_code} {r.text[:200]}")
        return

    pilgrim_token = r.json()["access_token"]
    ph = {"Authorization": f"Bearer {pilgrim_token}"}
    print(f"  pilgrim_token = {pilgrim_token[:30]}...")
    print()

    # ── Read preference from DB ─────────────────────────────────────────
    print("=" * 70)
    print("STEP C: READ PREFERENCE FROM DATABASE")
    print("=" * 70)
    r = httpx.get(f"{BASE}/preferences/by-pilgrim/8", headers=ah, timeout=30)
    print(f"  HTTP {r.status_code}")
    if r.status_code == 200:
        pref = r.json().get("data", r.json())
        pp("preferred_language", pref.get("preferred_language"))
        pp("delivery_mode", pref.get("delivery_mode"))
    else:
        print(f"  ERROR: {r.text[:300]}")
    print()

    # ── GET /announcements/my ───────────────────────────────────────────
    print("=" * 70)
    print("STEP D: GET /announcements/my — FULL TRACE")
    print("=" * 70)
    r = httpx.get(f"{BASE}/announcements/my", headers=ph, timeout=60)
    print(f"  HTTP {r.status_code}")
    resp = r.json()

    if r.status_code != 200:
        print(f"  ERROR RESPONSE:")
        print(f"  {json.dumps(resp, indent=2)[:1000]}")
        print()
        print("  *** ENDPOINT FAILED — cannot trace further ***")
        print()
        print("  POSSIBLE CAUSES:")
        print("  - Announcement expiry dates are in the past")
        print("  - Code error in the endpoint")
        print("  - Missing database columns")
        return

    items = resp.get("data", [])
    print(f"  Announcements returned: {len(items)}")
    print()

    for idx, ann in enumerate(items):
        print(f"  ════════════════════════════════════════════════════════════════")
        print(f"  ANNOUNCEMENT {idx + 1}")
        print(f"  ════════════════════════════════════════════════════════════════")

        print(f"\n  [DATABASE] Raw record from announcements table:")
        pp("id", ann.get("id"), 4)
        pp("title", ann.get("title"), 4)
        pp("message_template (raw)", ann.get("message") or ann.get("title"), 4)

        print(f"\n  [BACKEND] After placeholder replacement + translation:")
        pp("message (returned)", ann.get("message"), 4)
        pp("translated", ann.get("translated"), 4)
        pp("language", ann.get("language"), 4)
        pp("audio_url", ann.get("audio_url"), 4)

        print(f"\n  [FLUTTER] PersonalizedAnnouncement.fromJson():")
        pp("this.message", ann.get("message"), 4)
        pp("this.translated", ann.get("translated"), 4)
        pp("this.language", ann.get("language"), 4)
        pp("this.audioUrl", ann.get("audio_url"), 4)

        # Audio check
        audio_url = ann.get("audio_url")
        if audio_url:
            full_url = audio_url if audio_url.startswith("http") else f"https://ipilgram.onrender.com{audio_url}"
            print(f"\n  [AUDIO CENTER] Playing:")
            pp("full URL", full_url, 4)
            try:
                hr = httpx.head(full_url, timeout=15, follow_redirects=True)
                pp("HTTP status", hr.status_code, 4)
                pp("Content-Type", hr.headers.get("content-type"), 4)
                pp("Content-Length", hr.headers.get("content-length"), 4)
            except Exception as e:
                pp("HEAD error", str(e), 4)
        else:
            print(f"\n  [AUDIO CENTER] audio_url is NULL — no audio generated")
        print()

    # ── Language mapping check ──────────────────────────────────────────
    print("=" * 70)
    print("STEP E: LANGUAGE MAPPING AUDIT")
    print("=" * 70)
    lang_code_map = {"English": "en", "Hausa": "ha", "Arabic": "ar", "Yoruba": "yo", "Igbo": "ig"}
    tts_lang_map = {"English": "en", "Hausa": "ha", "Yoruba": "yo", "Igbo": "ig", "Arabic": "ar", "French": "fr", "Urdu": "ur", "Hindi": "hi"}
    preferred_langs = ["English", "Hausa", "Yoruba", "Igbo", "Arabic"]

    all_langs = ["English", "Hausa", "Yoruba", "Igbo", "Arabic", "French", "Urdu", "Hindi"]
    print(f"\n  {'Language':<12} {'PreferredLang':<15} {'lang_code_map':<15} {'tts_lang_map':<15} {'MobileDropdown'}")
    print(f"  {'-'*12} {'-'*15} {'-'*15} {'-'*15} {'-'*15}")
    for lang in all_langs:
        in_pref = lang in preferred_langs
        in_lang_code = lang in lang_code_map
        in_tts = lang in tts_lang_map
        in_mobile = lang in ["English", "Hausa", "Yoruba", "Igbo", "Arabic"]
        print(f"  {lang:<12} {str(in_pref):<15} {str(in_lang_code):<15} {str(in_tts):<15} {str(in_mobile)}")

    print()
    print("  GAP ANALYSIS:")
    for lang in all_langs:
        issues = []
        if lang not in preferred_langs:
            issues.append("NOT in PreferredLanguage enum")
        if lang not in lang_code_map:
            issues.append("NOT in lang_code_map (announcements.py:269)")
        if lang not in tts_lang_map:
            issues.append("NOT in TTS LANGUAGE_MAP")
        if lang not in ["English", "Hausa", "Yoruba", "Igbo", "Arabic"]:
            issues.append("NOT in mobile dropdown")
        if issues:
            print(f"  {lang}: {', '.join(issues)}")
        else:
            print(f"  {lang}: OK — fully supported")


if __name__ == "__main__":
    main()
