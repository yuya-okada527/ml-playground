from typing import List

from entrypoints.v1.movie.messages.movie_messages import MovieResponse, SimilarMovieResponse
from domain.enums.similarity_enums import SimilarityModelType
from service.logic.movie_logic import build_search_by_id_query, map_movie
from infra.client.solr.api import AbstractSolrClient
from infra.repository.redis_repository import AbstractKvsRepository


def exec_search_similar_service(
    movie_id: int,
    model_type: SimilarityModelType,
    kvs_repository: AbstractKvsRepository,
    solr_client: AbstractSolrClient
) -> SimilarMovieResponse:

    # KVSから類似映画IDを取得
    similar_movie_id_list = kvs_repository.get_similar_movie_id_list(
        movie_id=movie_id,
        model_type=model_type
    )

    # 類似映画を取得していく
    similar_movie_list = []
    for similar_id in similar_movie_id_list:
        
        # クエリを作成
        movie_id_query = build_search_by_id_query(movie_id=similar_id)

        # 検索結果を取得
        search_result = solr_client.search_movies(movie_id_query)

        # 取得件数を確認
        if len(search_result.response.docs) != 1:
            continue
        
        # 内部モデルに変換
        similar_movie_list.append(map_movie(search_result.response.docs[0]))

    return _map_response(
        movie_id=movie_id,
        model_type=model_type,
        similar_movie_list=similar_movie_list
    )


def _map_response(
    movie_id: int,
    model_type: SimilarityModelType,
    similar_movie_list: List[MovieResponse]
) -> SimilarMovieResponse:
    return SimilarMovieResponse(
        target_id=movie_id,
        model_type=model_type,
        results=similar_movie_list
    )
