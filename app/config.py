from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        validate_default=False,
    )
    ENV: str = 'dev'
    SQLALCHEMY_URI: PostgresDsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/app'

settings = Settings()