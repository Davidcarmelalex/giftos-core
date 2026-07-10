"""Application configuration using Pydantic Settings."""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """GiftOS Core configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "GiftOS Core"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://giftos:giftos@localhost:5432/giftos"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_POOL_SIZE: int = 50

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # NoOnes API
    NOONES_CLIENT_ID: str = ""
    NOONES_CLIENT_SECRET: str = ""
    NOONES_API_BASE: str = "https://api.noones.com"
    NOONES_AUTH_URL: str = "https://auth.noones.com/oauth2/token"
    NOONES_WEBHOOK_SECRET: str = ""

    # API Security
    API_RATE_LIMIT: str = "100/minute"
    API_KEY_HEADER: str = "X-API-Key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Scrapers
    SCRAPER_INTERVAL_SECONDS: int = 60
    SCRAPER_TIMEOUT_SECONDS: int = 30
    USER_AGENT: str = "GiftOS-Market-Intelligence/0.1.0"

    # Notifications
    TELEGRAM_BOT_TOKEN: str = ""
    WHATSAPP_API_KEY: str = ""
    ALERT_WEBHOOK_URL: str = ""

    # Monitoring
    SENTRY_DSN: str = ""
    LOG_LEVEL: str = "INFO"

    # CORS
    CORS_ORIGINS: List[str] = ["https://giftos.dev", "https://app.giftos.dev"]


settings = Settings()
