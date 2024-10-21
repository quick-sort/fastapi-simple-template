import os
import logging
from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

logger = logging.getLogger(__name__)
env_file = os.getenv('CONFIG_ENV_FILE', '.env')

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file,
        validate_default=False,
    )
    ENV: str = 'dev'
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'

    ## JWT TOKEN CONFIG
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: Literal['HS256'] = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    SESSION_COOKIE_NAME: str = 'session'

    ## DB CONFIG
    SQLALCHEMY_URI: PostgresDsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/app'

settings = Settings()

logging.basicConfig(
    format='%(levelname)s:%(asctime)s - %(filename)s:%(lineno)d:%(funcName)s %(message)s',
    encoding='utf-8',
    level=getattr(logging, settings.LOG_LEVEL.upper())
)
if os.path.exists(env_file):
    logger.info('loading settings from %s', env_file)
else:
    logger.info('loading settings from environments')
