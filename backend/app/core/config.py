"""
Application Configuration
Loads environment variables and provides settings for the application.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    groq_api_key: str = ""  # Set via GROQ_API_KEY in .env file
    
    # ChromaDB
    chroma_persist_dir: str = "./chroma_db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Groq Model
    groq_model: str = "llama-3.3-70b-versatile"
    
    # Docker Sandbox Settings
    sandbox_timeout: int = 5  # seconds
    sandbox_memory_limit: str = "128m"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
