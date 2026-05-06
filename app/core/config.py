import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management System"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./task_app.db"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY"
    ALGORITHM: str = "HS256"


settings = Settings()