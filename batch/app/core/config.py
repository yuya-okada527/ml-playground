from domain.enums.core_enums import LogLevel
from pydantic import BaseSettings


class CoreSettings(BaseSettings):
    batch_log_level: LogLevel

    class Config:
        env_file = "env/core.env"


class TmdbSettings(BaseSettings):
    tmdb_api_key: str
    tmdb_url: str = "https://api.themoviedb.org/3"

    class Config:
        env_file = "env/tmdb.env"


class InputDbSettings(BaseSettings):
    engine: str
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


class SolrSettings(BaseSettings):
    protocol: str = "http"
    host: str
    port: int
    collection: str

    def get_url(self):
        return f"{self.protocol}://{self.host}:{self.port}"

    class Config:
        env_file = "env/solr.env"


class RedisSettings(BaseSettings):
    redis_protocol: str
    redis_host: str
    redis_port: int

    class Config:
        env_file = "env/redis.env"
