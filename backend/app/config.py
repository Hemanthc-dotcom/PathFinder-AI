from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "Intelligent Career Counsellor API")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        self.cors_origins = [item.strip() for item in origins.split(",") if item.strip()]
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")


settings = Settings()
