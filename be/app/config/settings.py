from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "Todo API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./todo.db"
    DB_ECHO_LOG: bool = False

    CORS_ORIGINS: list[str] = ["*"]  # Allow all origins in development
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]


settings = Settings()
