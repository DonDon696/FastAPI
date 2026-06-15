from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    smtp_server: str
    smtp_port: int = 465
    smtp_user: str
    smtp_password: str
    to_email: str

    redis_url: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()