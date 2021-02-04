from typing import Protocol

from core.config import InputDbSettings
from domain.models.internal.movie import Genre
from domain.models.rdb.input import GenreRdbModel
from infra.repository.input.base import create_input_engine


UPSERT_GENRE_STATEMENT = """\
INSERT INTO 
    genres
VALUES
    (%(genre_id)s, %(name)s, %(japanese_name)s)
ON DUPLICATE KEY UPDATE
    `name` = %(name)s
  , `japanese_name` = %(japanese_name)s
"""


class AbstractGenreRepository(Protocol):
    
    def save(self, genre_list: list[GenreRdbModel]) -> None:
        ...
    
    def fetch_all(self) -> list[GenreRdbModel]:
        ...


class GenreRepository:

    def __init__(self, settings: InputDbSettings) -> None:
        self.engine = create_input_engine(settings)
    
    def save(self, genre_list: list[Genre]) -> int:

        count = 0
        for genre in genre_list:
            count += self.engine.execute(UPSERT_GENRE_STATEMENT, {
                "genre_id": genre.genre_id,
                "name": genre.name,
                "japanese_name": genre.japanese_name
            }).rowcount
        
        return count
    
    def fetch_all(self) -> list[GenreRdbModel]:
        ...
