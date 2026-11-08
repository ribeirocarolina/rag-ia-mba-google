from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_chat_model: str = Field(..., alias="OPENAI_CHAT_MODEL")
    openai_embedding_model: str = Field(..., alias="OPENAI_EMBEDDING_MODEL")
    database_url: str = Field(..., alias="DATABASE_URL")

    @property
    def psycopg_dsn(self) -> str:
        return self.database_url.replace("postgresql+psycopg://", "postgresql://")


settings = Settings()
