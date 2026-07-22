"""Project Fifty configuration module."""
from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API
    PROJECT_NAME: str = "Project Fifty"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/project_fifty"
    DATABASE_URL_SYNC: str = "postgresql+psycopg2://postgres:password@localhost:5432/project_fifty"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Mistral AI
    MISTRAL_API_KEY: str = ""
    MISTRAL_MODEL: str = "mistral-small-latest"
    MISTRAL_MAX_RETRIES: int = 3
    MISTRAL_TIMEOUT: int = 60

    # CrewAI
    CREW_VERBOSE: bool = True
    CREW_MAX_ITER: int = 10

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
