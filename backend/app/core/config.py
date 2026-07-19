from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Hajj Pilgrims API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    GEMINI_API_KEY: str = ""
    FIREBASE_CREDENTIALS_PATH: str = ""

    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        weak_defaults = {
            "hajj-pilgrims-dev-secret-key-change-in-production",
            "change-me",
            "secret",
            "changeme",
        }
        if v.lower() in weak_defaults or len(v) < 32:
            import logging
            logging.getLogger("hajj_api").warning(
                "SECRET_KEY is weak or default. Generate a strong key for production: "
                "python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        return v

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
