from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    APP_NAME: str = 'Secure Password Manager API'
    ENV: str = 'development'
    DATABASE_URL: str = 'sqlite:///./secure_vault.db'
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    FERNET_KEY: str
    RATE_LIMIT_DEFAULT: str = '100/minute'
    CORS_ORIGINS: str = 'http://localhost:3000,http://localhost:8081'


@lru_cache
def get_settings() -> Settings:
    return Settings()
