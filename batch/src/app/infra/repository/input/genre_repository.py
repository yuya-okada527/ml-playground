"""ジャンルリポジトリモジュール

映画ジャンルテーブルに対するアクセス機能を提供するモジュール
"""
from typing import Protocol

from domain.models.internal.movie_model import Genre
from infra.repository.input.base_repository import ENGINE
from sqlalchemy.engine.base import Engine

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
        """ジャンルリスト保存関数

        ジャンルマスタを保存します.

        Args:
            genre_list: 保存対象ジャンル
        """
        ...

    def fetch_all(self) -> list[Genre]:
        """ジャンル取得関数

        ジャンルマスタを全て取得します.
        """
        ...


class GenreRepository:

    def __init__(self, engine: Engine = ENGINE) -> None:
        self.engine: Engine = engine

    def save(self, genre_list: list[Genre]) -> int:

        count = 0
        for genre in genre_list:
            count += self.engine.execute(UPSERT_GENRE_STATEMENT, {
                "genre_id": genre.genre_id,
                "name": genre.name,
                "japanese_name": genre.japanese_name
            }).rowcount

        return count

    def fetch_all(self) -> list[Genre]:

        # SQL実行
        result = self.engine.execute(SELECT_ALL_GENRE_STATEMENT)

        # 内部モデルに変換
        genre_list = []
        for genre in result:
            genre_list.append(Genre(
                genre_id=genre.genre_id,
                name=genre.name,
                japanese_name=genre.japanese_name
            ))

        return genre_list
