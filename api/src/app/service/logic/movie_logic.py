"""映画ロジックモジュール

映画に関するロジックを記述するモジュール
"""
from typing import List

from domain.enums.movie_enums import MovieField
from domain.models.solr.movies import MovieSolrModel, SolrResultModel
from entrypoints.v1.movie.messages.movie_messages import (MovieResponse,
                                                          SearchMovieResponse)
from infra.client.solr.solr_query import (SEARCH_ALL, QueryParserType,
                                          SolrFilterQuery, SolrQuery)

# デフォルトの検索フィールド
DEFAULT_MOVIE_FLS = [
    MovieField.MOVIE_ID,
    MovieField.ORIGINAL_TITLE,
    MovieField.JAPANESE_TITLE,
    MovieField.OVERVIEW,
    MovieField.TAGLINE,
    MovieField.POSTER_PATH,
    MovieField.BACKDROP_PATH,
    MovieField.POPULARITY,
    MovieField.VOTE_AVERAGE,
    MovieField.RELEASE_DATE,
    MovieField.RELEASE_YEAR,
    MovieField.GENRES,
    MovieField.GENRE_LABELS,
    MovieField.KEYWORDS,
    MovieField.KEYWORD_LABELS
]


# TMDBの基盤画像URL
IMAGE_URL_BASE = "https://image.tmdb.org/t/p/w500"


def build_search_query(
    q: List[str],
    start: int,
    rows: int
) -> SolrQuery:
    """検索クエリを作成する.

    Args:
        q (List[str]): フリーワードクエリ
        start (int): 取得開始位置
        rows (int): 取得数

    Returns:
        SolrQuery: 検索クエリ
    """
    return SolrQuery(
        q=_build_free_word_query(q),
        fl=DEFAULT_MOVIE_FLS,
        start=start,
        rows=rows,
        defType=QueryParserType.EXTENDED_DISMAX,
        boost=MovieField.POPULARITY.value
    )


def build_search_by_id_query(movie_id: int) -> SolrQuery:
    """ID検索クエリを作成する.

    Args:
        movie_id (int): 映画ID

    Returns:
        SolrQuery: 検索クエリ
    """
    return SolrQuery(
        q=SolrFilterQuery.exact_condition(
            field=MovieField.MOVIE_ID,
            value=str(movie_id)
        ).get_query_string(),
        fl=DEFAULT_MOVIE_FLS,
        start=0,
        rows=1,
    )


def build_search_movie_id_query(start: int) -> SolrQuery:
    """全映画ID取得用のクエリを作成する.

    Args:
        start (int): 開始位置

    Returns:
        SolrQuery: 検索クエリ
    """
    return SolrQuery(
        q=SEARCH_ALL,
        fl=[MovieField.MOVIE_ID],
        start=start,
        rows=10
    )


def map_movie(movie: MovieSolrModel) -> MovieResponse:
    """映画レスポンスにマッピングする

    Args:
        movie (MovieSolrModel): Solrの映画モデル

    Returns:
        MovieResponse: 映画レスポンス
    """
    return MovieResponse(
        movie_id=movie.movie_id,
        original_title=movie.original_title,
        japanese_title=movie.japanese_title,
        overview=movie.overview,
        tagline=movie.tagline,
        poster_url=IMAGE_URL_BASE + movie.poster_path if movie.poster_path else None,
        backdrop_url=IMAGE_URL_BASE + movie.backdrop_path if movie.backdrop_path else None,
        popularity=movie.popularity,
        vote_average=movie.vote_average,
        release_date=movie.release_date,
        release_year=movie.release_year,
        genre_labels=movie.genre_labels,
        genres=movie.genres
    )


def map_search_movie_response(search_result: SolrResultModel) -> SearchMovieResponse:
    """映画検索レスポンスをマッピングする.

    Args:
        search_result (SolrResultModel): Solr検索結果

    Returns:
        SearchMovieResponse: 映画検索レスポンス
    """
    return SearchMovieResponse(
        start=search_result.response.start,
        returned_num=len(search_result.response.docs),
        available_num=search_result.response.numFound,
        results=[map_movie(movie) for movie in search_result.response.docs]
    )


def _build_free_word_query(q: List[str]) -> str:
    """フリーワードフィールドに対するクエリを作成する

    Args:
        q (List[str]): 検索クエリリスト

    Returns:
        str: クエリ文字列
    """
    # 未指定の場合、全検索
    if not q:
        return SEARCH_ALL

    # 指定ありの場合、フリーワードのAND検索を構築する
    return " AND ".join(f"{MovieField.FREE_WORD.value}:{query}" for query in q)
