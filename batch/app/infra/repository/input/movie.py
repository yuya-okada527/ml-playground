from typing import Protocol
import logging

from sqlalchemy.exc import IntegrityError

from core.config import InputDbSettings
from domain.models.internal.movie import Movie
from infra.repository.input.base import INPUT_APPS, create_input_engine

# TODO ロギング制御
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


UPSERT_MOVIE_STATEMENT = """\
INSERT INTO
    movies
VALUES
    (
        %(movie_id)s,
        %(imdb_id)s,
        %(original_title)s,
        %(japanese_title)s,
        %(overview)s,
        %(tagline)s,
        %(poster_path)s,
        %(backdrop_path)s,
        %(popularity)s,
        %(vote_average)s,
        %(vote_count)s
    )
ON DUPLICATE KEY UPDATE
    imdb_id = %(imdb_id)s,
    original_title = %(original_title)s,
    japanese_title = %(japanese_title)s,
    overview = %(overview)s,
    tagline = %(tagline)s,
    poster_path = %(poster_path)s,
    backdrop_path = %(backdrop_path)s,
    popularity = %(popularity)s,
    vote_average = %(vote_average)s,
    vote_count = %(vote_count)s
"""

INSERT_MOVIE_GENRE_STATEMENT = """\
INSERT INTO
    movie_genres
VALUES
    (
        %(movie_id)s,
        %(genre_id)s
    )
"""


class AbstractMovieRepository(Protocol):
    
    def save_movie_list(self, movie_list: list[Movie]):
        ...


class MovieRepository:
    
    def __init__(self, settings: InputDbSettings) -> None:
        self.engine = create_input_engine(settings)
    
    def save_movie_list(self, movie_list: list[Movie]):

        movie_count = 0
        genre_count = 0
        for movie in movie_list:
            movie_count += self.engine.execute(UPSERT_MOVIE_STATEMENT, {
                "movie_id": movie.movie_id,
                "imdb_id": movie.imdb_id,
                "original_title": movie.original_title,
                "japanese_title": movie.japanese_title,
                "overview": movie.overview,
                "tagline": movie.tagline,
                "poster_path": movie.poster_path,
                "backdrop_path": movie.backdrop_path,
                "popularity": movie.popularity,
                "vote_average": movie.vote_average,
                "vote_count": movie.vote_count
            }).rowcount

            for genre in movie.genres:
                try:
                    genre_count += self.engine.execute(INSERT_MOVIE_GENRE_STATEMENT, {
                        "movie_id": movie.movie_id,
                        "genre_id": genre.genre_id
                    }).rowcount
                except IntegrityError:
                    pass
                

