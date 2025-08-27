from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    BRW_BASE_URL: str = "https://apicast.rw.by/v1/"
    BRW_USER_KEY: str = "c11f8d06e3e1594815b9c4ebaddf19a0" # key for app identification
    BOT_TOKEN: str

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def API_TIMEOUT(self) -> float:
        from random import uniform
        return 10.0 + uniform(0.0, 0.5)

    model_config = SettingsConfigDict(env_file=env_path)

settings = Settings() # pyright: ignore[reportCallIssue]
__all__ = ["settings"]
