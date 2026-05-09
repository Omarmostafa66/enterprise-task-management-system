import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Project metadata
    PROJECT_NAME: str = "Task Management System"

    # Database configuration
    # Uses Docker environment variable if available,
    # otherwise falls back to local MySQL connection
    SQLALCHEMY_DATABASE_URL: str = os.getenv(
        "SQLALCHEMY_DATABASE_URL",
        "mysql+pymysql://root:@localhost:3306/task_db"
    )

    # Redis configuration
    # Supports both local development and Docker environments
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    # JWT security configuration
    # Reads SECRET_KEY from environment variables or .env file
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "CHANGE_THIS_SECRET_IN_PRODUCTION"
    )

    ALGORITHM: str = "HS256"

    # Load environment variables from .env file automatically
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()