from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AskHR Production API"
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # Defaults to gemini, matches your ingest.py
    LLM_PROVIDER: str = "gemini" 

    @property
    def CHROMA_PATH(self) -> str:
        if self.LLM_PROVIDER.lower() == "openai":
            return "./data/chroma_db_openai"
        return "./data/chroma_db_google"

    # Allow extra fields if they exist in .env but aren't defined here
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()