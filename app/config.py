from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_minutes: int
    allow_origin = []
    class Config:
        env_file = ".env"


settings = Settings()
