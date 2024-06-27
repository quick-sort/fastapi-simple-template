from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        validate_default=False,
    )
    ENV: str = 'dev'

    ## JWT TOKEN CONFIG
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: Literal['HS256'] = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    ## DB CONFIG
    SQLALCHEMY_URI: PostgresDsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/app'

settings = Settings()