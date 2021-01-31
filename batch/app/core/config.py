from pydantic import BaseSettings


class TmdbSettings(BaseSettings):
    tmdb_api_key: str
    tmdb_url: str = "https://api.themoviedb.org/3"

    class Config:
        env_file = "env/tmdb.env"


class InputDbSettings(BaseSettings):
    engine: str = "tortoise.backends.mysql"
    host: str
    port: int
    db_user: str
    password: str
    database: str
    echo: bool


    class Config:
        env_file = "env/input_db.env"

