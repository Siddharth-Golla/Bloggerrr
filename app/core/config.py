from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Bloggerrr"
    debug: bool = True
    database_url: str = "sqlite:///./bloggerrr.db"


settings = Settings()
