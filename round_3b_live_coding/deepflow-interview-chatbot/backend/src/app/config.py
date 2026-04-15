import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://chatbot:chatbot@localhost:5433/chatbot"
    )
    OPENROUTER_API_KEY: str = Field(default="")
    INNGEST_DEV: bool = Field(default=True)

    DB_DATA_DIR: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent / "db"
    )

    model_config = {
        "env_file": str(Path(__file__).resolve().parent.parent.parent / ".env"),
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()

if settings.OPENROUTER_API_KEY:
    os.environ["OPENROUTER_API_KEY"] = settings.OPENROUTER_API_KEY
