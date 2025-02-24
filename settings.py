from enum import Enum
import os
from pydantic import Field
from pydantic_settings import BaseSettings

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
    DB_DRIVER: str = Field(default="postgresql+psycopg2")
    DB_ECHO: bool = Field(default=False)  # SQL query logging

    # Redis settings (if you're using Redis)
    CACHE_HOST: str = Field(default="localhost")
    CACHE_PORT: int = Field(default=6379)
    CACHE_DB: int = Field(default=0)

    # JWT settings
    JWT_SECRET: str = Field(default="your_secret_key")
    JWT_ALGORITHM: str = Field(default="HS256")


    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            # Use .local.env by default, .prod.env if ENV=prod
            # Set the env file path based on environment
            env_file = f".{os.getenv('ENV', 'local')}.env"
            # Configure env_file in Config class
            cls.env_file = env_file
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )

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


# Create a global settings instance
settings = Settings()
    
        