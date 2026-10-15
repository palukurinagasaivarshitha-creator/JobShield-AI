import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "Fake Job Detection & Verification Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"

    # Database: Defaults to SQLite for seamless local dev; can use Postgres URL via environment
    DATABASE_URL: str = "sqlite:///./fake_jobs.db"

    # Machine Learning and Datasets
    MODEL_PATH: str = str(BASE_DIR.parent / "models" / "fake_job_detector.joblib")
    DATASET_PATH: str = str(BASE_DIR.parent / "data" / "emscad_dataset.csv")
    SEED_DATASET_PATH: str = str(BASE_DIR.parent / "data" / "seed_jobs.csv")

    # Safe Scraping & Network Limits
    MAX_CONTENT_LENGTH_BYTES: int = 2 * 1024 * 1024  # 2 MB limit
    REQUEST_TIMEOUT_SECONDS: int = 8
    USER_AGENT: str = "FakeJobVerifierBot/1.0 (+https://fakejobverifier.local)"

    @property
    def cors_origin_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
