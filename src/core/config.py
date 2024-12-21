from pathlib import Path
from typing import Literal, Optional

from dotenv import load_dotenv
from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings

#  Load environment variables from .env file
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # --- App Settings ---
    APP_NAME: str = "Wallet"
    MODE: Literal["DEV", "TEST", "PROD"] = "TEST"

    # --- Database Settings ---
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_URL: Optional[str] = None

    # --- Auth Settings ---
    SECRET_TOKEN: str

    # --- Other Settings ---
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_URL: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def assemble_db_urls(cls, values):
        # Формируем значения для DB_URL и TEST_DB_URL
        if not values.get("DB_URL"):
            values["DB_URL"] = (
                f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}"
                f"@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
            )

        if not values.get("TEST_DB_URL"):
            values["TEST_DB_URL"] = (
                f"postgresql+asyncpg://{values['TEST_DB_USER']}:{values['TEST_DB_PASS']}"
                f"@{values['TEST_DB_HOST']}:{values['TEST_DB_PORT']}/{values['TEST_DB_NAME']}"
            )

        return values

    model_config = ConfigDict(env_file=str(env_path))


settings = Settings()
