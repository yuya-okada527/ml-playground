from typing import Protocol

from tortoise import Tortoise, run_async
from tortoise.exceptions import OperationalError
from tortoise.transactions import atomic, in_transaction

from core.config import InputDbSettings
from domain.models.internal.movie import Genre
from domain.models.rdb.input import GenreRdbModel


class AbstractGenreRepository(Protocol):
    
    def save(self, genre_list: list[GenreRdbModel]):
        ...


class GenreRepository:

    def __init__(self, settings: InputDbSettings) -> None:
        self.connections = {
            "default": {
                "engine": settings.engine,
                "credentials": {
                    "host": settings.host,
                    "port": settings.port,
                    "user": settings.db_user,
                    "password": settings.password,
                    "database": settings.database,
                    "echo": settings.echo
                }
            }
        }
    
    def save(self, genre_list: list[Genre]):
        async def run_save():
            # DBをセットアップ
            await Tortoise.init(
                config={
                    "connections": self.connections,
                    "apps": {
                        "input": {
                            "models": ["domain.models.rdb.input"],
                            "default_connection": "default"
                        }
                    }
                }
            )
            try:
                async with in_transaction() as connection:
                    for genre in genre_list:
                        genre_rdb = GenreRdbModel(
                            genre_id=genre.genre_id, 
                            name=genre.name, 
                            japanese_name=genre.japanese_name
                        )
                        await genre_rdb.save(using_db=connection, update_fields=["name", "japanese_name"])
            except OperationalError as e:
                raise e
            saved_genre = await GenreRdbModel.all()
            print(saved_genre)
        
        run_async(run_save())

