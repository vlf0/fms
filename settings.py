"""Resbonsible for reading and representing secrets from .env file."""
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


# pylint: disable=R0903
class Settings(BaseSettings):
    """A class to represent application settings."""

    kis_db_url: str = 'default'
    jwt_secret_key: str = 'default'

    class Config:
        """Represent rows of variables from .env file."""

        env_file = ".env"


settings = Settings()
