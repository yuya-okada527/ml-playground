"""検索サービスモジュール

検索に関するサービス関数を記述するモジュール
"""
from typing import List

from domain.exceptions.service_exception import NoTargetException
from domain.models.solr.movies import SolrResultModel
from entrypoints.v1.movie.messages.movie_messages import (MovieResponse,
                                                          SearchMovieResponse)
from infra.client.solr.solr_api import AbstractSolrClient

from service.logic.movie_logic import (build_search_by_id_query,
                                       build_search_query, map_movie,
                                       map_movie_response)

# TMDBの基盤画像URL
IMAGE_URL_BASE = "https://image.tmdb.org/t/p/w500"


def exec_search_service(
    q: List[str],
    start: int,
    rows: int,
    solr_client: AbstractSolrClient
) -> SearchMovieResponse:
    """検索サービスを実行する

    Args:
        q (List[str]): 検索クエリ
        start (int): 取得開始位置(0始まり)
        rows (int): 取得件数
        solr_client (AbstractSolrClient): Solrクライアント

    Returns:
        SearchMovieResponse: レスポンス
    """

    # クエリの構築
    solr_query = build_search_query(q=q, start=start, rows=rows)

    # 検索実行
    search_result = solr_client.search_movies(solr_query)

    return map_movie_response(search_result)


def exec_search_by_id_service(
    movie_id: int,
    solr_client: AbstractSolrClient
) -> MovieResponse:
    """映画IDによる検索サービスを実行する

    Args:
        movie_id (int): 映画ID
        solr_client (AbstractSolrClient): Solrクライアント

    Raises:
        NoTargetException: 取得対象のデータがない場合に発生する

    Returns:
        MovieResponse: レスポンス
    """

    # クエリの構築
    solr_query = build_search_by_id_query(movie_id)

    # 検索実行
    search_result = solr_client.search_movies(solr_query)

    # 取得件数を確認
    if len(search_result.response.docs) != 1:
        raise NoTargetException()

    return map_movie(search_result.response.docs[0])
