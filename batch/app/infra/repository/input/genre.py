from typing import Protocol

from tortoise import Tortoise, run_async
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction

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

            # 登録・更新数を記録
            update_count = 0
            insert_count = 0

            try:
                async with in_transaction() as connection:
                    for genre in genre_list:
                        genre_rdb = GenreRdbModel(
                            genre_id=genre.genre_id, 
                            name=genre.name, 
                            japanese_name=genre.japanese_name
                        )

                        # 更新対象が存在するかで分岐
                        target = await GenreRdbModel.filter(genre_id=genre.genre_id)
                        if target:
                            # 更新
                            # TODO ハッシュを比較して、更新処理を制御
                            update_count += 1
                            await genre_rdb.save(using_db=connection, update_fields=["name", "japanese_name"])
                        else:
                            # 登録
                            insert_count += 1
                            await genre_rdb.save(using_db=connection)
            except OperationalError as e:
                raise e
            print(f"登録数={insert_count}, 更新数={update_count}")
        
        run_async(run_save())
