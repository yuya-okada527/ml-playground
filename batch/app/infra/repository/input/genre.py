from typing import Protocol

from domain.models.internal.movie import Genre
from infra.repository.input.base import ENGINE


# ---------------------------
# SQL
# ---------------------------
UPSERT_GENRE_STATEMENT = """\
INSERT INTO
    genres
VALUES
    (%(genre_id)s, %(name)s, %(japanese_name)s)
ON DUPLICATE KEY UPDATE
    name = %(name)s,
    japanese_name = %(japanese_name)s
"""

SELECT_ALL_GENRE_STATEMENT = """\
SELECT
    genre_id,
    name,
    japanese_name
FROM
    genres
"""


class AbstractGenreRepository(Protocol):

    def save(self, genre_list: list[Genre]) -> int:
        ...

    def fetch_all(self) -> list[Genre]:
        ...


class GenreRepository:

    def save(self, genre_list: list[Genre]) -> int:

        count = 0
        for genre in genre_list:
            count += ENGINE.execute(UPSERT_GENRE_STATEMENT, {
                "genre_id": genre.genre_id,
                "name": genre.name,
                "japanese_name": genre.japanese_name
            }).rowcount

        return count

    def fetch_all(self) -> list[Genre]:

        # SQL実行
        result = ENGINE.execute(SELECT_ALL_GENRE_STATEMENT)

        # 内部モデルに変換
        genre_list = []
        for genre in result:
            genre_list.append(Genre(
                genre_id=genre.genre_id,
                name=genre.name,
                japanese_name=genre.japanese_name
            ))

        return genre_list
