from pydantic import BaseModel, ConfigDict, Field

from app.models.preference import PreferredLanguage


class SimplifyRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Original Hajj announcement text", examples=["Check-in starts at 14:00 at Hilton Makkah"])
    language: PreferredLanguage = Field(
        default=PreferredLanguage.English,
        description="Target language for simplification",
        examples=["English"],
    )


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to translate", examples=["Your flight departs at 8:00 AM"])
    target_language: PreferredLanguage = Field(..., description="Target language for translation", examples=["Hausa"])
    source_language: PreferredLanguage = Field(default=PreferredLanguage.English, description="Source language", examples=["English"])


class ProcessRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Original Hajj announcement", examples=["Flight AP-201 departs at 08:00"])
    target_language: PreferredLanguage = Field(default=PreferredLanguage.English, description="Target language for output", examples=["English"])
    audio_required: bool = Field(default=False, description="Whether audio output is needed", examples=[False])


class PilgrimQueryRequest(BaseModel):
    query: str = Field(
        ..., min_length=2, max_length=2000,
        description="Pilgrim's question about their own data (flight, accommodation, transport, announcements)",
        examples=["What time is my flight?"],
    )


class AIQueryResponse(BaseModel):
    response: str = Field(..., description="AI-generated response based on pilgrim's own authorized data")
    category: str = Field(..., description="Response category: flight, accommodation, transport, announcement, general, unsupported")
    language: str = Field(..., description="Language of the response")
    audio_required: bool = Field(..., description="Whether audio output should be generated")


class ProcessResponse(BaseModel):
    text: str = Field(..., description="Processed and simplified text")
    language: str = Field(..., description="Output language")
    audio_required: bool = Field(..., description="Whether audio output was requested")
    category: str = Field(default="general", description="Content category")


class SimplifyResponse(BaseModel):
    original: str = Field(..., description="Original text input")
    simplified: str = Field(..., description="Simplified text output")
    language: str = Field(..., description="Output language")
    model_used: str = Field(default="", description="AI model identifier")


class TranslateResponse(BaseModel):
    original: str = Field(..., description="Original text input")
    translated: str = Field(..., description="Translated text output")
    source_language: str = Field(..., description="Source language")
    target_language: str = Field(..., description="Target language")
    model_used: str = Field(default="", description="AI model identifier")


class HealthCheckResponse(BaseModel):
    provider: str = Field(..., description="AI provider name (e.g. gemini, openai)")
    configured: bool = Field(..., description="Whether the API key is configured")

    model_config = ConfigDict(from_attributes=True)
