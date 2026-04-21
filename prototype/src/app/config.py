from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "local"
    app_port: int = 8000
    database_url: str
    sync_database_url: str
    log_level: str = "INFO"
    worker_poll_seconds: int = 5

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
