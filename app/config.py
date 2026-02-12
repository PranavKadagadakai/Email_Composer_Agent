import os

from dotenv import load_dotenv
from pydantic import EmailStr, Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    # Gemini
    GEMINI_API_KEY: str = Field(..., min_length=10)

    # SMTP
    SMTP_SERVER: str = Field(..., min_length=3)
    SMTP_PORT: int = Field(..., ge=1, le=65535)
    SMTP_USER: EmailStr
    SMTP_PASSWORD: str = Field(..., min_length=8)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


def get_settings() -> Settings:
    """
    Load and validate application settings.
    Fail fast if configuration is invalid.
    """
    try:
        return Settings(
            GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY"),
            SMTP_SERVER=os.environ.get("SMTP_SERVER"),
            SMTP_PORT=int(os.environ.get("SMTP_PORT")),
            SMTP_USER=os.environ.get("SMTP_USER"),
            SMTP_PASSWORD=os.environ.get("SMTP_PASSWORD"),
        )
    except ValidationError as e:
        raise RuntimeError(f"Configuration Error:\n{e}")
