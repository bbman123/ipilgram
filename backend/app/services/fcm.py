import os
import json
import time
from typing import Any

import httpx
import jwt


class FCMService:
    """Firebase Cloud Messaging via HTTP v1 API.

    Uses a service account JSON to obtain an OAuth2 token,
    then sends messages via FCM HTTP v1 endpoint.
    No firebase-admin SDK required.
    """

    SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    FCM_URL = "https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    def __init__(self):
        self._service_account: dict | None = None
        self._access_token: str | None = None
        self._token_expiry: float = 0
        self._client = httpx.Client(timeout=10)

    def _load_service_account(self) -> dict:
        if self._service_account is None:
            path = os.environ.get("FIREBASE_CREDENTIALS_PATH", "")
            if not path:
                raise ValueError("FIREBASE_CREDENTIALS_PATH not set")
            with open(path) as f:
                self._service_account = json.load(f)
        return self._service_account

    def _get_access_token(self) -> str:
        if self._access_token and time.time() < self._token_expiry:
            return self._access_token

        sa = self._load_service_account()
        now = int(time.time())
        payload = {
            "iss": sa["client_email"],
            "scope": " ".join(self.SCOPES),
            "aud": self.TOKEN_URL,
            "iat": now,
            "exp": now + 3600,
        }
        signed_jwt = jwt.encode(payload, sa["private_key"], algorithm="RS256")

        resp = self._client.post(self.TOKEN_URL, data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": signed_jwt,
        })
        resp.raise_for_status()
        data = resp.json()

        self._access_token = data["access_token"]
        self._token_expiry = time.time() + data.get("expires_in", 3600) - 60
        return self._access_token

    def is_configured(self) -> bool:
        path = os.environ.get("FIREBASE_CREDENTIALS_PATH", "")
        return bool(path and os.path.exists(path))

    def send_to_token(self, token: str, title: str, body: str, data: dict | None = None) -> dict:
        """Send a notification to a single device token."""
        access_token = self._get_access_token()
        sa = self._load_service_account()
        project_id = sa.get("project_id", "")

        message: dict[str, Any] = {
            "token": token,
            "notification": {"title": title, "body": body},
        }
        if data:
            message["data"] = {k: str(v) for k, v in data.items()}

        payload = {"message": message}

        resp = self._client.post(
            self.FCM_URL.format(project_id=project_id),
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        resp.raise_for_status()
        return resp.json()

    def send_to_tokens(self, tokens: list[str], title: str, body: str, data: dict | None = None) -> list[dict]:
        """Send to multiple tokens individually. Returns list of responses."""
        results = []
        for token in tokens:
            try:
                result = self.send_to_token(token, title, body, data)
                results.append({"token": token, "success": True, "response": result})
            except Exception as e:
                results.append({"token": token, "success": False, "error": str(e)})
        return results
