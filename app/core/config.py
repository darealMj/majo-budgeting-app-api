import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MAJO Budgeting App API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # fallback on localdev SQLite instead of prod PostGreSQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./budgeting.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()
