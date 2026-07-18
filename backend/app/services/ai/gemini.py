import httpx

from app.services.ai.base import AIProvider, AIResponse


class GeminiProvider(AIProvider):
    """Google Gemini API provider.

    Uses the REST API directly via httpx — no SDK dependency.
    Set GEMINI_API_KEY in .env to authenticate.
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    MODEL = "gemini-2.0-flash"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client(timeout=30)

    def generate(self, prompt: str, system_instruction: str = "") -> AIResponse:
        url = f"{self.BASE_URL}/{self.MODEL}:generateContent?key={self.api_key}"

        contents = []
        if system_instruction:
            contents.append({
                "role": "user",
                "parts": [{"text": system_instruction}],
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Understood. I will follow these instructions."}],
            })

        contents.append({
            "role": "user",
            "parts": [{"text": prompt}],
        })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048,
            },
        }

        resp = self.client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]
        token_count = data.get("usageMetadata", {}).get("totalTokenCount", 0)

        return AIResponse(text=text.strip(), model=self.MODEL, tokens_used=token_count)
