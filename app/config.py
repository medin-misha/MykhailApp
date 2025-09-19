from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # конфигурация BaseSettings
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    postgres_url: str
    rabbit_url: str


settings = Settings()