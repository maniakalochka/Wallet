from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

from pathlib import Path

#  Load environment variables from .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # --- App Settings ---
    APP_NAME: str = "Wallet"

    # --- Database Settings ---
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASS")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_URL = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    ECHO: bool = True
    EXPIRE_ON_COMMIT: bool = False

    # --- Other Settings ---
    DEBUG: bool = True
    IS_TESTING: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
