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

    def get_connection_config(self):
        return {
            "default": {
                "engine": self.engine,
                "credentials": {
                    "host": self.host,
                    "port": self.port,
                    "user": self.db_user,
                    "password": self.password,
                    "database": self.database
                }
            }
        }


    class Config:
        env_file = "env/input_db.env"

