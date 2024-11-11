from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import ClassVar
import os

from pathlib import Path

#  Load environment variables from .env file
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # --- App Settings ---
    APP_NAME: str = "Wallet"

    # --- Database Settings ---
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_URL: ClassVar[str]

    ECHO: bool = True
    EXPIRE_ON_COMMIT: bool = False

    # --- Auth Settings ---
    SECRET_TOKEN: str

    # --- Other Settings ---
    DEBUG: bool = True
    IS_TESTING: bool = True

    class Config:
        env_file = str(env_path)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Settings.DB_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
