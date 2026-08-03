"""Temporary debug endpoint to verify Gemini connectivity and inspect raw responses.

This endpoint is for development/diagnostic use only.
Remove before production deployment.
"""

import logging
import traceback
import time

from fastapi import APIRouter, Query

from app.core.config import get_settings
from app.services.ai.gemini import GeminiProvider, GeminiError
from app.services.translation import translate_text, get_cache_stats, clear_cache

logger = logging.getLogger("hajj_api")

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/gemini")
def debug_gemini():
    """Build a tiny prompt, call Gemini, return raw response with types."""
    settings = get_settings()
    api_key = settings.GEMINI_API_KEY

    result = {
        "environment": {
            "ai_enabled": bool(api_key),
            "gemini_model": "gemini-3.5-flash",
            "api_key_exists": bool(api_key),
            "api_key_length": len(api_key) if api_key else 0,
            "provider": "gemini",
            "timeout": 30,
            "temperature": 0.3,
            "max_tokens": 2048,
        },
    }

    if not api_key:
        result["error"] = "GEMINI_API_KEY not configured"
        return result

    try:
        provider = GeminiProvider(api_key)
    except GeminiError as e:
        result["error"] = f"Provider init failed: {e.message}"
        result["details"] = e.details
        return result

    test_prompt = "Say hello in exactly 5 words."

    start_time = time.time()
    try:
        ai_response = provider.generate(test_prompt, "")
        elapsed = time.time() - start_time

        result["status"] = "success"
        result["elapsed_seconds"] = round(elapsed, 2)
        result["response"] = {
            "text": ai_response.text,
            "text_type": type(ai_response.text).__name__,
            "text_length": len(ai_response.text),
            "model": ai_response.model,
            "model_type": type(ai_response.model).__name__,
            "tokens_used": ai_response.tokens_used,
            "tokens_used_type": type(ai_response.tokens_used).__name__,
        }
    except GeminiError as e:
        elapsed = time.time() - start_time
        result["status"] = "gemini_error"
        result["elapsed_seconds"] = round(elapsed, 2)
        result["error"] = e.message
        result["error_status_code"] = e.status_code
        result["error_details"] = e.details
    except Exception as e:
        elapsed = time.time() - start_time
        result["status"] = "unexpected_error"
        result["elapsed_seconds"] = round(elapsed, 2)
        result["error"] = str(e)
        result["error_type"] = type(e).__name__
        result["traceback"] = traceback.format_exc()

    return result


@router.get("/translate")
def debug_translate(
    text: str = Query("Hello, your flight departs at 8:00 AM", description="Text to translate"),
    language: str = Query("Hausa", description="Target language"),
):
    """Test translation endpoint. Translates text to the target language."""
    start_time = time.time()
    try:
        translated = translate_text(text, language)
        elapsed = time.time() - start_time
        return {
            "status": "success",
            "elapsed_seconds": round(elapsed, 2),
            "input": {
                "text": text,
                "language": language,
                "text_length": len(text),
            },
            "output": {
                "translated": translated,
                "translated_length": len(translated),
                "was_translated": translated != text,
            },
            "cache": get_cache_stats(),
        }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "status": "error",
            "elapsed_seconds": round(elapsed, 2),
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc(),
        }


@router.post("/translate/cache/clear")
def debug_clear_translation_cache():
    """Clear the translation cache."""
    clear_cache()
    return {"status": "ok", "message": "Translation cache cleared"}
