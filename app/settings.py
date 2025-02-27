from enum import Enum
import os
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings
from typing import Optional


class EnvironmentType(str, Enum):
    LOCAL = "local"
    PROD = "prod"


class Settings(BaseSettings):
    # Environment settings
    ENV: EnvironmentType = EnvironmentType.LOCAL

    # Database settings
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="password")
    DB_NAME: str = Field(default="pomodoro")
    DB_DRIVER: str = Field(default="postgresql+asyncpg")
    DB_ECHO: bool = Field(default=True)  # SQL query logging

    # Redis settings (if you're using Redis)
    CACHE_HOST: str = Field(default="localhost")
    CACHE_PORT: int = Field(default=6379)
    CACHE_DB: int = Field(default=0)

    # JWT settings
    JWT_SECRET: str = Field(default="your_secret_key")
    JWT_ALGORITHM: str = Field(default="HS256")

    # Google settings
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None)
    GOOGLE_SECRET_KEY: Optional[str] = Field(default=None)
    GOOGLE_REDIRECT_URI: Optional[str] = Field(default=None)
    GOOGLE_TOKEN_URL: str = Field(default="https://accounts.google.com/o/oauth2/token")
    GOOGLE_USER_INFO_URL: str = Field(default="https://www.googleapis.com/oauth2/v3/userinfo")

    # Add this to store the current env file
    ENV_FILE: str = f".{os.getenv('ENV', 'local')}.env"

    class Config:
        env_file = f".{os.getenv('ENV', 'local')}.env"
        extra = "allow"

    @model_validator(mode='after')
    def validate_google_settings(self):
        if not all([self.GOOGLE_CLIENT_ID, self.GOOGLE_SECRET_KEY, self.GOOGLE_REDIRECT_URI]):
            raise ValueError(
                "Required Google OAuth settings are missing. "
                f"Please check your {self.Config.env_file} file contains GOOGLE_CLIENT_ID, "
                "GOOGLE_SECRET_KEY, and GOOGLE_REDIRECT_URI"
            )
        return self

    @property
    def is_production(self) -> bool:
        return self.ENV == EnvironmentType.PROD

    @property
    def get_db_url(self) -> str:
        """Construct database URL from settings."""
        return (
            f"{self.DB_DRIVER}://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    @property
    def get_google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"

# Create a global settings instance
settings = Settings()

