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

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier (e.g. 'gemini', 'openai')."""
        ...

    @abstractmethod
    def generate(self, prompt: str, system_instruction: str = "") -> AIResponse:
        """Send a prompt to the AI and return the response text."""
        ...

    @abstractmethod
    def is_configured(self) -> bool:
        """Check if the provider has valid credentials."""
        ...
