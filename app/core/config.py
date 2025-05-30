import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "MAJO Budgeting App API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./budgeting.db")

    # Security configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS configuration
    CORS_ORIGINS: list = ["*"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
