"""検索サービスモジュール

検索に関するサービス関数を記述するモジュール
"""
from typing import List

from domain.exceptions.service_exception import NoTargetException
from entrypoints.v1.movie.messages.movie_messages import (MovieIdResponse,
                                                          MovieResponse,
                                                          SearchMovieResponse)
from infra.client.solr.solr_api import AbstractSolrClient

from service.logic.movie_logic import (build_search_by_id_query,
                                       build_search_movie_id_query,
                                       build_search_query, map_movie,
                                       map_search_movie_response)


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

    return map_search_movie_response(search_result)


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


def exec_search_movie_ids(solr_client: AbstractSolrClient) -> MovieIdResponse:

    # 映画IDリストを初期化
    movie_ids = []

    # startを0で初期化
    start = 0
    while True:
        # クエリを作成
        query = build_search_movie_id_query(start=start)

        # 検索実行
        movies = solr_client.search_movies(query=query)

        # 映画IDリストを更新
        movie_ids.extend([movie.movie_id for movie in movies.response.docs])

        # 取得開始位置を更新
        start = len(movie_ids)

        # 最後まで取得できたか判定
        if len(movie_ids) >= movies.response.numFound:
            break

    return MovieIdResponse(movie_ids=movie_ids)
