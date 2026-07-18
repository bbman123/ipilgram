from abc import ABC, abstractmethod

from pydantic import BaseModel


class AIResponse(BaseModel):
    text: str
    model: str = ""
    tokens_used: int = 0


class AIProvider(ABC):
    """Abstract base class for AI providers.

    Implement this interface to swap AI backends (Gemini, OpenAI, etc.)
    without changing the personalization engine.
    """

    @abstractmethod
    async def generate(self, prompt: str, system_instruction: str = "") -> AIResponse:
        """Send a prompt to the AI and return the response text."""
        ...
