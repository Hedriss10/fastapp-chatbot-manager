# app/settings/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_uri: str

    authentication_api_key: str
    url_instance_evolution: str
    evolution_apikey: str
    url_webapp: str

    host_redis: str
    port_redis: int
    db_redis: int
    socke_connect_timeout: int
    rate_count_limit_message: int
    closes_message_redis: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    url_frontend: str
    url_vite_frontend: str

    class Config:
        env_file = ".env"


settings = Settings()
