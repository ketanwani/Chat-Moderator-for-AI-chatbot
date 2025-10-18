from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/moderation_db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # ML Models
    ML_MODEL_CACHE_DIR: str = "./model_cache"

    # Redis (for caching)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Performance thresholds
    MODERATION_LATENCY_THRESHOLD_MS: int = 100

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Moderation and Compliance Engine"

    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
