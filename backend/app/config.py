"""
config.py
=========
Centralised application configuration.

Every value that could differ between a developer's laptop, a teammate's
machine in another city, and a future deployment on Render / Railway is
read from environment variables here — nothing is hardcoded anywhere
else in the codebase.

Usage
-----
    from app.config import settings

    settings.APP_NAME
    settings.CORS_ORIGINS
    settings.PORT
"""

import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings, populated from environment variables (or a
    local `.env` file during development — see `.env.example`).
    """

    # ── General ────────────────────────────────────────────────────────
    APP_NAME: str = "Mars Rover Monitoring & Navigation Backend"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development | production

    # ── Server ─────────────────────────────────────────────────────────
    # Render / Railway inject PORT automatically at runtime. Locally it
    # defaults to 8000. HOST stays 0.0.0.0 so the server is reachable
    # both locally and inside a container.
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── CORS ───────────────────────────────────────────────────────────
    # Comma separated list of allowed origins, e.g.:
    #   CORS_ORIGINS=http://localhost:8501,https://my-dashboard.streamlit.app
    # Use "*" (default) while the team is developing from different
    # cities/networks; tighten this before shipping to production.
    CORS_ORIGINS_RAW: str = "*"

    @property
    def CORS_ORIGINS(self) -> List[str]:
        if self.CORS_ORIGINS_RAW.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS_RAW.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings accessor. Using lru_cache means the .env file /
    environment is only read once per process, then reused everywhere
    the settings are imported.
    """
    return Settings()


settings = get_settings()
