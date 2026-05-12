import json
from typing import Literal, Optional

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AskHR Production API"
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    APP_ENV: Literal["development", "staging", "production"] = "development"
    CORS_ALLOW_ORIGINS: list[str] | str = Field(default_factory=lambda: ["http://localhost:8088"])
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # Defaults to gemini, matches your ingest.py
    LLM_PROVIDER: Literal["gemini", "openai"] = "gemini"

    @field_validator("CORS_ALLOW_ORIGINS", mode="before")
    @classmethod
    def parse_cors_allow_origins(cls, value: object) -> object:
        # Support both JSON arrays and comma-separated strings from environment variables.
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.startswith("["):
                try:
                    return json.loads(stripped)
                except json.JSONDecodeError:
                    pass
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @model_validator(mode="after")
    def validate_provider_and_keys(self) -> "Settings":
        provider = self.LLM_PROVIDER
        if provider == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        if provider == "gemini" and not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required when LLM_PROVIDER=gemini")
        if self.CORS_ALLOW_CREDENTIALS and "*" in self.CORS_ALLOW_ORIGINS:
            raise ValueError("CORS_ALLOW_ORIGINS cannot contain '*' when CORS_ALLOW_CREDENTIALS is true")
        if self.APP_ENV == "production":
            if not self.CORS_ALLOW_ORIGINS:
                raise ValueError("CORS_ALLOW_ORIGINS must contain at least one explicit origin when APP_ENV=production")
            if any("localhost" in origin.lower() or "127.0.0.1" in origin for origin in self.CORS_ALLOW_ORIGINS):
                raise ValueError("CORS_ALLOW_ORIGINS must not include localhost/127.0.0.1 when APP_ENV=production")
            if any("*" in origin for origin in self.CORS_ALLOW_ORIGINS):
                raise ValueError("CORS_ALLOW_ORIGINS cannot include wildcard values when APP_ENV=production")
        return self

    @property
    def CHROMA_PATH(self) -> str:
        if self.LLM_PROVIDER == "openai":
            return "./data/chroma_db_openai"
        return "./data/chroma_db_google"

    # Allow extra fields if they exist in .env but aren't defined here
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()