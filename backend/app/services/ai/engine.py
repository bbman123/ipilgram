import json
import re

from app.services.ai.base import AIProvider, AIResponse


SYSTEM_INSTRUCTION = """You are a Hajj pilgrimage information assistant for Nigerian pilgrims.

RULES:
- You ONLY process official Hajj-related information (announcements, flights, accommodations, transport, emergencies).
- You do NOT answer general knowledge questions.
- You do NOT engage in casual conversation.
- If the input is not Hajj-related, respond with: "I can only help with Hajj-related information."
- Always respond in the SAME language as the input unless explicitly asked to translate.
- Keep responses short, clear, and action-oriented.
- Use simple words that anyone can understand.
- For dates/times, use 12-hour format with AM/PM.
- For translations, preserve the meaning exactly — do not add or remove information."""


class PersonalizationEngine:
    """Processes Hajj information through an AI provider.

    Functions:
    - simplify: Make announcements easier to understand
    - translate: Translate between supported languages
    - process: Full pipeline → simplify + translate + structured JSON
    """

    SUPPORTED_LANGUAGES = ["English", "Hausa", "Yoruba", "Igbo", "Arabic"]

    def __init__(self, provider: AIProvider):
        self.provider = provider

    def simplify(self, text: str, language: str = "English") -> AIResponse:
        """Simplify a Hajj announcement into plain, clear language."""
        prompt = f"""Simplify the following Hajj announcement for {language}-speaking pilgrims from Nigeria.

Make it:
- Short and clear
- Use simple, everyday words
- Include actionable instructions
- Keep the same language ({language})
- Preserve all important details (times, locations, flight numbers)

Original:
{text}

Simplified version in {language}:"""

        return self.provider.generate(prompt, SYSTEM_INSTRUCTION)

    def translate(self, text: str, target_language: str, source_language: str = "English") -> AIResponse:
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

        return self.provider.generate(prompt, SYSTEM_INSTRUCTION)

    def process(self, text: str, target_language: str = "English", audio_required: bool = False) -> dict:
        """Full pipeline: simplify → translate → return structured JSON.

        Returns:
            {
                "text": "...",
                "language": "...",
                "audio_required": bool
            }
        """
        # Step 1: Simplify
        simplified = self.simplify(text, "English")
        simplified_text = simplified.text

        # Step 2: Translate if target is not English
        if target_language != "English":
            translated = self.translate(simplified_text, target_language, "English")
            final_text = translated.text
        else:
            final_text = simplified_text

        return {
            "text": final_text,
            "language": target_language,
            "audio_required": audio_required,
        }
