from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        validate_default=False,
    )
    ENV: str = 'dev'

settings = Settings()