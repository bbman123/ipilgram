import os

from app.services.ai.base import AIProvider, AIResponse


class OpenAIProvider(AIProvider):
    """OpenAI API provider stub.

    Implements the AIProvider interface for future use.
    Requires OPENAI_API_KEY in .env to authenticate.
    """

    MODEL = "gpt-4o-mini"

    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def name(self) -> str:
        return "openai"

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, system_instruction: str = "") -> AIResponse:
        # Stub — not yet implemented. Returns placeholder.
        # To implement: use httpx to call OpenAI's chat completions API
        # following the same pattern as GeminiProvider.
        raise NotImplementedError(
            "OpenAI provider is not yet implemented. "
            "Set OPENAI_API_KEY and implement the generate() method."
        )
