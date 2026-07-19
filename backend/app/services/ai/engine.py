import json
import re
import logging

from sqlalchemy.orm import Session

from app.services.ai.base import AIProvider, AIResponse
from app.services.ai.context import build_pilgrim_context, PilgrimContext

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """You are a Hajj pilgrimage information assistant for Nigerian pilgrims.

RULES:
- You ONLY have access to the pilgrim's own data provided in the context below.
- You ONLY answer questions about the pilgrim's own flight, accommodation, transport, package, and relevant announcements.
- You do NOT answer questions about other pilgrims.
- You do NOT answer general knowledge questions unrelated to Hajj logistics.
- You do NOT engage in casual conversation.
- If the question is not about the pilgrim's own data, respond with: "I can only help with your Hajj-related information."
- Always respond in the pilgrim's preferred language.
- Keep responses short, clear, and action-oriented.
- Use simple words that anyone can understand.
- For dates/times, use 12-hour format with AM/PM.

You MUST respond in the following JSON format exactly:
{
  "response": "your answer here",
  "category": "flight|accommodation|transport|announcement|general|unsupported",
  "audio_required": true or false
}

Set audio_required to true if the message is important or the pilgrim asked for audio.
Always set audio_required to true for announcements and emergencies."""


class PersonalizationEngine:
    """Processes pilgrim queries through an AI provider using only authorized context.

    Workflow:
    1. Build restricted context from pilgrim's own data
    2. Send query + context to AI provider
    3. Parse structured JSON response
    """

    def __init__(self, provider: AIProvider):
        self.provider = provider

    def answer_query(self, pilgrim_id: int, query: str, db: Session) -> dict:
        """Answer a pilgrim's question using only their authorized data.

        Steps:
        1. Build context from DB (pilgrim sees only their own data)
        2. Send to AI with system instruction
        3. Parse JSON response
        """
        ctx = build_pilgrim_context(pilgrim_id, db)

        prompt = f"""PIGRIM DATA:
{ctx.to_prompt_context()}

PIGRIM'S QUESTION:
{query}

Respond in JSON format."""

        target_language = "English"
        if ctx.preference and ctx.preference.preferred_language:
            target_language = ctx.preference.preferred_language.value

        ai_response = self.provider.generate(prompt, SYSTEM_INSTRUCTION)

        parsed = self._parse_response(ai_response.text)
        parsed["language"] = target_language

        logger.info(
            "AI query processed: pilgrim=%d, category=%s, tokens=%d",
            pilgrim_id, parsed.get("category", "unknown"), ai_response.tokens_used,
        )
        return parsed

    def process(self, text: str, target_language: str = "English", audio_required: bool = False) -> dict:
        """Full pipeline for admin-driven processing (backward compat).

        Returns structured JSON with text, language, and audio flag.
        """
        prompt = f"""Simplify and translate the following Hajj announcement for {target_language}-speaking pilgrims from Nigeria.

Make it short, clear, and actionable. Preserve all important details (times, locations, flight numbers).
If target is not English, translate to {target_language}.

Text:
{text}

Respond in JSON format:
{{
  "response": "simplified text here",
  "category": "announcement",
  "audio_required": {str(audio_required).lower()}
}}"""

        ai_response = self.provider.generate(prompt, SYSTEM_INSTRUCTION)
        parsed = self._parse_response(ai_response.text)
        parsed["language"] = target_language

        return parsed

    def simplify(self, text: str, target_language: str = "English") -> dict:
        """Simplify a Hajj announcement into plain, clear language."""
        prompt = f"""Simplify the following Hajj announcement for {target_language}-speaking pilgrims from Nigeria.

Make it:
- Short and clear
- Use simple, everyday words
- Include actionable instructions
- Keep the same language ({target_language})
- Preserve all important details (times, locations, flight numbers)

Original:
{text}

Simplified version in {target_language}:"""

        ai_response = self.provider.generate(prompt, SYSTEM_INSTRUCTION)
        parsed = self._parse_response(ai_response.text)
        parsed["language"] = target_language
        return parsed

    def translate(self, text: str, target_language: str, source_language: str = "English") -> dict:
        """Translate Hajj information to the target language."""
        prompt = f"""Translate the following Hajj information from {source_language} to {target_language}.

Rules:
- Preserve the exact meaning
- Keep proper nouns (flight numbers, hotel names, place names) as-is
- Use natural phrasing for {target_language} speakers
- Keep numbers and times the same

Text to translate:
{text}

Translation in {target_language}:"""

        ai_response = self.provider.generate(prompt, SYSTEM_INSTRUCTION)
        parsed = self._parse_response(ai_response.text)
        parsed["language"] = target_language
        return parsed

    def _parse_response(self, text: str) -> dict:
        """Parse AI response text into structured JSON.

        Falls back to raw text if JSON parsing fails.
        """
        try:
            cleaned = re.sub(r"```json\n?|\n?```", "", text.strip())
            data = json.loads(cleaned)
            return {
                "response": data.get("response", cleaned),
                "category": data.get("category", "general"),
                "audio_required": data.get("audio_required", False),
            }
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning("Failed to parse AI JSON response: %s", exc)
            return {
                "response": text.strip(),
                "category": "general",
                "audio_required": False,
            }
