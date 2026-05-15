from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # For easy testing this uses SQLite by default. Put MySQL URL in .env for production.
    DATABASE_URL: str = "sqlite:///./ai_forecasting.db"
    SECRET_KEY: str = "change-this-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    UPLOAD_DIR: str = "app/uploads"
    REPORT_DIR: str = "app/reports"

    class Config:
        env_file = ".env"

settings = Settings()
