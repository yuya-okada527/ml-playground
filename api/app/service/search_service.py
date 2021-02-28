from typing import List

from domain.exceptions.service_exception import NoTargetException
from domain.models.solr.movies import SolrResultModel
from entrypoints.v1.movie.messages.movie_messages import (MovieResponse,
                                                          SearchMovieResponse)
from infra.client.solr.api import AbstractSolrClient

from service.logic.movie_logic import (build_search_by_id_query,
                                       build_search_query, map_movie)

IMAGE_URL_BASE = "https://image.tmdb.org/t/p/w500"


def exec_search_service(
    q: List[str],
    start: int,
    rows: int,
    solr_client: AbstractSolrClient
) -> SearchMovieResponse:

    # クエリの構築
    solr_query = build_search_query(q=q, start=start, rows=rows)

    # 検索実行
    search_result = solr_client.search_movies(solr_query)

    return _map_response(search_result)


def exec_search_by_id_service(movie_id: int, solr_client: AbstractSolrClient) -> MovieResponse:

    # クエリの構築
    solr_query = build_search_by_id_query(movie_id)

    # 検索実行
    search_result = solr_client.search_movies(solr_query)

    # 取得件数を確認
    if len(search_result.response.docs) != 1:
        raise NoTargetException()

    return map_movie(search_result.response.docs[0])


def _map_response(search_result: SolrResultModel) -> SearchMovieResponse:
    return SearchMovieResponse(
        start=search_result.response.start,
        returned_num=len(search_result.response.docs),
        available_num=search_result.response.numFound,
        results=[map_movie(movie) for movie in search_result.response.docs]
    )
