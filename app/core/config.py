from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Bloggerrr"
    debug: bool = True


settings = Settings()