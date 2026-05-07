from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SentimentIQ"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-for-local-dev"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_NAME: str = "sentimentiq"
    REDIS_URL: str = "redis://localhost:6379/0"

    FRONTEND_URL: str = "http://localhost:5173"
    CACHE_TTL_SECONDS: int = 45
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads"

    VADER_NEGATIVE_THRESHOLD: float = -0.15
    VADER_POSITIVE_THRESHOLD: float = 0.15
    SENTIMENT_DROP_THRESHOLD: float = -0.18
    ASPECT_DROP_THRESHOLD: float = -0.12
    REALTIME_POLL_SECONDS: int = 15

    TRANSFORMER_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"
    ENABLE_TRANSFORMERS: bool = True
    ENABLE_BERTOPIC: bool = True
    BERTOPIC_MIN_REVIEWS: int = 8

    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "admin123"
    DEMO_USER_EMAIL: str = "analyst@example.com"
    DEMO_USER_PASSWORD: str = "demo123"

    DEFAULT_SAMPLE_CSV: str = "../sample_data/reviews_sample.csv"
    DEFAULT_SAMPLE_JSON: str = "../sample_data/reviews_sample.json"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    @property
    def backend_dir(self) -> Path:
        return Path(__file__).resolve().parents[1]

    @property
    def project_root(self) -> Path:
        return self.backend_dir.parent

    @property
    def upload_path(self) -> Path:
        return self.backend_dir / self.UPLOAD_DIR


settings = Settings()
