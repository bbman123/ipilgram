from pydantic import BaseModel, Field

from app.models.preference import PreferredLanguage


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    language: PreferredLanguage = Field(default=PreferredLanguage.english)


class TTSResponse(BaseModel):
    audio_url: str
    language: str
    cached: bool = False
