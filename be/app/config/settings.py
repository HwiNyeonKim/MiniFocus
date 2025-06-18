from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "MiniFocus"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./todo.db"
    DB_ECHO_LOG: bool = False

    SECRET_KEY: str = "temp-secret-key-for-dev"  # TODO: Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]


settings = Settings()
