# app/settings/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_uri: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    url_frontend: str
    url_vite_frontend: str
    backend_base_url: str
    cors_origins_: str
    cors_origins: str

    class Config:
        env_file = '.env'


settings = Settings()
