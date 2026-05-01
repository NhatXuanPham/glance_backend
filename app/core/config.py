from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str

    # OAuth (optional)
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str | None = None

    ZALO_CLIENT_ID: str | None = None
    ZALO_CLIENT_SECRET: str | None = None

    TIKTOK_CLIENT_ID: str | None = None
    TIKTOK_CLIENT_SECRET: str | None = None

    FRONTEND_URL: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()