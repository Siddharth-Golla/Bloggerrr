from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Bloggerrr"
    debug: bool = True
    database_url: str = "sqlite:///./bloggerrr.db"

    secret_key: str = "development-secret-change-later-123"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
