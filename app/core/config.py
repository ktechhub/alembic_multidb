# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = "1.0.0"
    CONTACT: dict = {
        "name": "KtechHub FastAPI Demo",
        "url": "https://www.ktechhub.com/",
        "email": "info@ktechhub.com",
    }

    ENV: str = "dev"

    if ENV == "dev":
        RELOAD: bool = True
        LOG_LEVEL: str = "debug"
    else:
        RELOAD: bool = False
        LOG_LEVEL: str = "info"

    ALLOWED_HOSTS: list = ["*"]

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_URL: str = ""

    class Config:
        env_file = "./.env"
        extra = "ignore"


settings = Settings()
settings.DATABASE_URL = f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
