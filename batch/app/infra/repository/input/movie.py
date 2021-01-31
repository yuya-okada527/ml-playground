from typing import Protocol

from tortoise import Tortoise, run_async
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction

from core.config import InputDbSettings
from domain.models.internal.movie import Movie
from domain.models.rdb.input import MovieGenreRdbModel, MovieRdbModel
from infra.repository.input.base import INPUT_APPS


class AbstractMovieRepository(Protocol):
    
    def save_movie_list(self, movie_list: list[Movie]):
        ...


class MovieRepository:
    
    def __init__(self, settings: InputDbSettings) -> None:
        self.connections = settings.get_connection_config()
    
    def save_movie_list(self, movie_list: list[Movie]):
        async def run_save_movie_list():
            # DBをセットアップ
            await Tortoise.init(
                config={
                    "connections": self.connections,
                    "apps": INPUT_APPS
                }
            )

            # 登録・更新数を記録
            update_count = 0
            insert_count = 0

            for movie in movie_list:
                try:
                    async with in_transaction() as connection:
                        movie_rdb = MovieRdbModel(
                            tmdb_id=movie.tmdb_id,
                            imdb_id=movie.imdb_id,
                            original_title=movie.original_title,
                            japanese_title=movie.japanese_title,
                            overview=movie.overview,
                            tagline=movie.tagline,
                            poster_path=movie.poster_path,
                            backdrop_path=movie.backdrop_path,
                            popularity=movie.popularity,
                            vote_average=movie.vote_average,
                            vote_count=movie.vote_count
                        )

                        # 更新対象が存在するかで分岐
                        target_movie = await MovieRdbModel.filter(tmdb_id=movie.tmdb_id)
                        if target_movie:
                            # 存在する場合はスキップ
                            update_count += 1
                            continue
                        else:
                            # 登録
                            await movie_rdb.save(using_db=connection)
                            for genre in movie.genres:
                                movie_genre_rdb = MovieGenreRdbModel(
                                    movie_id=movie_rdb.movie_id,
                                    genre_id=genre.genre_id
                                )
                                await movie_genre_rdb.save(using_db=connection)
                            insert_count += 1
                except OperationalError as e:
                    raise e
            print(f"登録数={insert_count}, 更新数={update_count}")
        run_async(run_save_movie_list())

