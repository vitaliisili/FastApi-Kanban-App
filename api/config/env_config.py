from pydantic import BaseSettings


class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str
    token_secret_key: str
    token_algorithm: str
    token_expire_minutes: int

    class Config:
        env_file = '.env'


settings = Settings()
