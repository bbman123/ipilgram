import logging
from typing import Any

import httpx

from app.services.ai.base import AIProvider, AIResponse

logger = logging.getLogger("hajj_api")


class GeminiError(Exception):
    """Raised when the Gemini API returns an error."""

    def __init__(self, message: str, status_code: int = 502, details: Any = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class GeminiProvider(AIProvider):
    """Google Gemini API provider.

    Uses the REST API directly via httpx — no SDK dependency.
    Set GEMINI_API_KEY in .env to authenticate.

    Model: gemini-3.5-flash (stable, free-tier eligible).
    Docs: https://ai.google.dev/gemini-api/docs/models/gemini-v2
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    MODEL = "gemini-3.5-flash"

    def __init__(self, api_key: str):
        if not api_key:
            raise GeminiError(
                message="GEMINI_API_KEY is empty",
                status_code=503,
                details={"reason": "api_key_missing"},
            )
        self.api_key = api_key
        self.client = httpx.Client(timeout=30)
        logger.info(
            "GeminiProvider initialized: model=%s, api_key_present=True, api_key_length=%d",
            self.MODEL,
            len(api_key),
        )

    @property
    def name(self) -> str:
        return "gemini"

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, system_instruction: str = "") -> AIResponse:
        logger.info(
            "Entering GeminiProvider.generate: prompt_type=%s, prompt_length=%d, has_system_instruction=%s",
            type(prompt).__name__,
            len(prompt),
            bool(system_instruction),
        )

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

        logger.info("Sending HTTP POST to Gemini API...")
        try:
            resp = self.client.post(url, json=payload)
        except httpx.TimeoutException:
            logger.error("Gemini API timeout after 30s")
            raise GeminiError(
                message="AI service timed out. Please try again.",
                status_code=504,
                details={"reason": "timeout"},
            )
        except httpx.ConnectError as e:
            logger.error("Gemini API connection error: %s", str(e))
            raise GeminiError(
                message="Unable to connect to AI service.",
                status_code=502,
                details={"reason": "connection_error", "error": str(e)},
            )
        except httpx.HTTPError as e:
            logger.error("Gemini API HTTP error: %s", str(e))
            raise GeminiError(
                message="AI service communication error.",
                status_code=502,
                details={"reason": "http_error", "error": str(e)},
            )

        logger.info("Gemini API response: status_code=%d", resp.status_code)

        if resp.status_code != 200:
            body = resp.text
            logger.error(
                "Gemini API returned HTTP %d: %s",
                resp.status_code,
                body[:500],
            )

            if resp.status_code == 400:
                raise GeminiError(
                    message="Invalid request to AI service.",
                    status_code=502,
                    details={"reason": "bad_request", "raw": body[:300]},
                )
            elif resp.status_code == 403:
                raise GeminiError(
                    message="AI service access denied. Check API key permissions.",
                    status_code=502,
                    details={"reason": "forbidden", "raw": body[:300]},
                )
            elif resp.status_code == 404:
                raise GeminiError(
                    message=f"AI model '{self.MODEL}' not found. The model may have been renamed or removed.",
                    status_code=502,
                    details={"reason": "model_not_found", "model": self.MODEL, "raw": body[:300]},
                )
            elif resp.status_code == 429:
                raise GeminiError(
                    message="AI service rate limit exceeded. Try again later.",
                    status_code=429,
                    details={"reason": "rate_limited", "raw": body[:300]},
                )
            elif resp.status_code >= 500:
                raise GeminiError(
                    message="AI service is temporarily unavailable.",
                    status_code=502,
                    details={"reason": "server_error", "status": resp.status_code, "raw": body[:300]},
                )
            else:
                raise GeminiError(
                    message="AI provider error.",
                    status_code=502,
                    details={"reason": "unknown", "status": resp.status_code, "raw": body[:300]},
                )

        logger.info("Parsing Gemini response JSON...")
        try:
            data = resp.json()
        except Exception as e:
            logger.error("Gemini response is not valid JSON: %s", str(e))
            raise GeminiError(
                message="AI service returned invalid response.",
                status_code=502,
                details={"reason": "invalid_json"},
            )

        logger.info(
            "Gemini response data type=%s, keys=%s",
            type(data).__name__,
            list(data.keys()) if isinstance(data, dict) else "N/A",
        )

        candidates = data.get("candidates")
        if not candidates:
            prompt_feedback = data.get("promptFeedback", {})
            block_reason = prompt_feedback.get("blockReason")
            if block_reason:
                logger.warning("Gemini blocked prompt: %s", block_reason)
                raise GeminiError(
                    message="AI service blocked the request due to content policy.",
                    status_code=400,
                    details={"reason": "blocked", "block_reason": block_reason},
                )
            logger.error("Gemini returned no candidates. Full response: %s", str(data)[:500])
            raise GeminiError(
                message="AI service returned an empty response.",
                status_code=502,
                details={"reason": "no_candidates"},
            )

        logger.info(
            "Gemini candidates count=%d, candidate type=%s",
            len(candidates),
            type(candidates[0]).__name__,
        )

        candidate = candidates[0]

        finish_reason = candidate.get("finishReason")
        logger.info("Gemini finishReason=%s", finish_reason)
        if finish_reason and finish_reason != "STOP":
            logger.warning("Gemini finished with reason: %s", finish_reason)

        content = candidate.get("content")
        logger.info("Gemini content type=%s", type(content).__name__ if content else "None")
        if not content:
            logger.error("Gemini candidate has no content: %s", str(candidate)[:500])
            raise GeminiError(
                message="AI service returned empty content.",
                status_code=502,
                details={"reason": "no_content"},
            )

        parts = content.get("parts")
        logger.info("Gemini parts type=%s, count=%d", type(parts).__name__ if parts else "None", len(parts) if parts else 0)
        if not parts:
            logger.error("Gemini content has no parts: %s", str(content)[:500])
            raise GeminiError(
                message="AI service returned empty content.",
                status_code=502,
                details={"reason": "no_parts"},
            )

        for i, part in enumerate(parts):
            logger.info(
                "Gemini part[%d] type=%s, keys=%s",
                i,
                type(part).__name__,
                list(part.keys()) if isinstance(part, dict) else "N/A",
            )

        text = parts[0].get("text", "")
        logger.info(
            "Gemini text type=%s, length=%d",
            type(text).__name__,
            len(text),
        )
        if not text.strip():
            logger.error("Gemini returned empty text")
            raise GeminiError(
                message="AI service returned empty response.",
                status_code=502,
                details={"reason": "empty_text"},
            )

        usage = data.get("usageMetadata", {})
        token_count = usage.get("totalTokenCount", 0)
        logger.info(
            "Gemini usageMetadata: promptTokenCount=%s, candidatesTokenCount=%s, totalTokenCount=%s",
            usage.get("promptTokenCount"),
            usage.get("candidatesTokenCount"),
            token_count,
        )

        result = AIResponse(text=text.strip(), model=self.MODEL, tokens_used=token_count)
        logger.info(
            "Returning AIResponse: type=%s, text_length=%d, model=%s, tokens_used=%d",
            type(result).__name__,
            len(result.text),
            result.model,
            result.tokens_used,
        )
        return result
