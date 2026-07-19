from pydantic import BaseModel, ConfigDict, Field

from app.models.preference import PreferredLanguage


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech", examples=["Welcome to Hajj 2026"])
    language: PreferredLanguage = Field(default=PreferredLanguage.english, description="Target language for speech synthesis")


class TTSResponse(BaseModel):
    audio_url: str = Field(..., description="URL path to download the generated audio file")
    language: str = Field(..., description="Language of the generated audio")
    cached: bool = Field(default=False, description="Whether this was served from cache")

    model_config = ConfigDict(from_attributes=True)
