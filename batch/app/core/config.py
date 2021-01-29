from pydantic import BaseSettings


class Settings(BaseSettings):
    # TMDb
    tmdb_api_key: str
    tmdb_url: str = "https://api.themoviedb.org/3"

    class Config:
        env_file = ".env"


settings = Settings()