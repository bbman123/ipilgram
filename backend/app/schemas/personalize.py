from pydantic import BaseModel, Field

from app.models.preference import PreferredLanguage


class SimplifyRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Original Hajj announcement text")
    language: PreferredLanguage = Field(
        default=PreferredLanguage.english,
        description="Target language for simplification"
    )


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    target_language: PreferredLanguage
    source_language: PreferredLanguage = PreferredLanguage.english


class ProcessRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Original Hajj announcement")
    target_language: PreferredLanguage = PreferredLanguage.english
    audio_required: bool = Field(default=False, description="Whether audio output is needed")


class ProcessResponse(BaseModel):
    text: str
    language: str
    audio_required: bool


class SimplifyResponse(BaseModel):
    original: str
    simplified: str
    language: str
    model_used: str = ""


class TranslateResponse(BaseModel):
    original: str
    translated: str
    source_language: str
    target_language: str
    model_used: str = ""
