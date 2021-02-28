"""映画レポジトリモジュール

映画テーブルに対するアクセス機能を提供するモジュール
"""
from collections import defaultdict
from datetime import datetime
from typing import Protocol

from domain.models.internal.movie_model import RELEASE_DATE_FMT, Genre, Movie
from infra.repository.input.base_repository import ENGINE
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.result import RowProxy
from sqlalchemy.exc import IntegrityError

# ---------------------------
# SQL
# ---------------------------
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
        %(vote_count)s,
        %(release_date)s
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
    vote_count = %(vote_count)s,
    release_date = %(release_date)s
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

SELECT_ALL_MOVIE_STATEMENT = """\
SELECT
    m.movie_id,
    m.imdb_id,
    m.original_title,
    m.japanese_title,
    m.overview,
    m.tagline,
    m.poster_path,
    m.backdrop_path,
    m.popularity,
    m.vote_average,
    m.vote_count,
    m.release_date,
    g.genre_id,
    g.name,
    g.japanese_name,
    sm.similar_movie_id
FROM
    movies AS m
    INNER JOIN
        movie_genres AS mg
        ON m.movie_id = mg.movie_id
    INNER JOIN
        genres AS g
        ON mg.genre_id = g.genre_id
    INNER JOIN
        similar_movies AS sm
        ON m.movie_id = sm.movie_id
"""

SELECT_ALL_MOVIE_ID_STATEMENT = """\
SELECT
    m.movie_id
FROM
    movies AS m
"""

INSERT_SIMILAR_MOVIE_STATEMENT = """\
INSERT INTO
    similar_movies
VALUES
    (
        %(movie_id)s,
        %(similar_movie_id)s
    )
"""

SELECT_ALL_SIMILAR_MOVIE_STATEMENT = """\
SELECT
    sm.movie_id,
    sm.similar_movie_id
FROM
    similar_movies AS sm
"""


class AbstractMovieRepository(Protocol):

    def save_movie_list(self, movie_list: list[Movie]) -> None:
        """映画リストを保存します.

        Args:
            movie_list: 映画リスト
        """
        ...

    def save_similar_movie_list(
        self,
        movie_id: int,
        similar_movie_list: list[int]
    ) -> int:
        """類似映画リストを保存します.

        Args:
            movie_id: 映画ID
            similar_movie_list: 類似映画IDリスト
        """
        ...

    def fetch_all(self) -> list[Movie]:
        """全映画情報を取得します."""
        ...

    def fetch_all_movie_id(self) -> list[int]:
        """全映画IDを取得します."""
        ...

    def fetch_all_similar_movie(self) -> dict[int, list[int]]:
        """全映画とその類似映画を取得する

        Returns:
            類似映画dict(key: movie_id, value: set(similar_movie_id))
        """
        ...


class MovieRepository:

    def __init__(self, engine: Engine = ENGINE) -> None:
        self.engine: Engine = engine

    def save_movie_list(self, movie_list: list[Movie]) -> None:

        movie_count = 0
        genre_count = 0
        for movie in movie_list:
            # TODO トランザクション
            # TODO リトライ
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
                "vote_count": movie.vote_count,
                "release_date": movie.release_date_str
            }).rowcount

            for genre in movie.genres:
                try:
                    genre_count += self.engine.execute(INSERT_MOVIE_GENRE_STATEMENT, {
                        "movie_id": movie.movie_id,
                        "genre_id": genre.genre_id
                    }).rowcount
                except IntegrityError:
                    # 重複データの登録は無視する
                    pass

    def save_similar_movie_list(
        self,
        movie_id: int,
        similar_movie_list: list[int]
    ) -> int:

        count = 0
        with self.engine.begin() as conn:
            for similar_movie_id in similar_movie_list:
                try:
                    count += conn.execute(INSERT_SIMILAR_MOVIE_STATEMENT, {
                        "movie_id": movie_id,
                        "similar_movie_id": similar_movie_id
                    }).rowcount
                except IntegrityError:
                    # 重複データの登録は無視する
                    pass

        return count

    def fetch_all(self) -> list[Movie]:

        # SQL実行
        result_proxy = self.engine.execute(SELECT_ALL_MOVIE_STATEMENT)

        # movie_idごとに取得結果を管理、映画情報にジャンルと類似映画を追加していく
        movie_map = {}
        for result in result_proxy:
            if result.movie_id not in movie_map:
                movie_map[result.movie_id] = _map_to_movie(result)
            else:
                movie_map[result.movie_id].genres.append(_map_to_genre(result))
                movie_map[result.movie_id].similar_movies.append(result.similar_movie_id)

        result = []
        for movie in movie_map.values():
            movie.genres = list(set(movie.genres))
            movie.similar_movies = list(set(movie.similar_movies))
            result.append(movie)
        return result

    def fetch_all_movie_id(self) -> list[int]:

        # SQL実行
        result_proxy = self.engine.execute(SELECT_ALL_MOVIE_ID_STATEMENT)

        return [movie.movie_id for movie in result_proxy]

    def fetch_all_similar_movie(self) -> dict[int, list[int]]:

        # SQL実行
        result_proxy = self.engine.execute(SELECT_ALL_SIMILAR_MOVIE_STATEMENT)

        # 類似映画MAPを作成 (key: movie_id, value: list(similar_movie_id))
        similar_movies = defaultdict(list)
        for row in result_proxy:
            similar_movies[row.movie_id].append(row.similar_movie_id)

        return similar_movies


def _map_to_movie(result: RowProxy) -> Movie:
    return Movie(
        movie_id=result.movie_id,
        imdb_id=result.imdb_id,
        original_title=result.original_title,
        japanese_title=result.japanese_title,
        overview=result.overview,
        tagline=result.tagline,
        poster_path=result.poster_path,
        backdrop_path=result.backdrop_path,
        popularity=result.popularity,
        vote_average=result.vote_average,
        vote_count=result.vote_count,
        release_date=datetime.strptime(result.release_date, RELEASE_DATE_FMT) if result.release_date else None,
        genres=[_map_to_genre(result)],
        similar_movies=[int(result.similar_movie_id)]
    )


def _map_to_genre(result: RowProxy) -> Genre:
    return Genre(
        genre_id=result.genre_id,
        name=result.name,
        japanese_name=result.japanese_name
    )
