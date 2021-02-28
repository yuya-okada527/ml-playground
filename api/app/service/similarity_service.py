"""類似性データサービスモジュール

類似性データに関するサービス関数を記述するモジュール
"""

from domain.enums.similarity_enums import SimilarityModelType
from entrypoints.v1.movie.messages.movie_messages import SimilarMovieResponse
from infra.client.solr.solr_api import AbstractSolrClient
from infra.repository.kvs_repository import AbstractKvsRepository

from service.logic.similarity_logic import (fetch_similar_movies,
                                            map_similar_movies_response)


def exec_search_similar_service(
    movie_id: int,
    model_type: SimilarityModelType,
    kvs_repository: AbstractKvsRepository,
    solr_client: AbstractSolrClient
) -> SimilarMovieResponse:
    """類似映画検索サービス

    Args:
        movie_id (int): 映画ID
        model_type (SimilarityModelType): 類似映画判定モデルタイプ
        kvs_repository (AbstractKvsRepository): KVSリポジトリ
        solr_client (AbstractSolrClient): Solrクライアント

    Returns:
        SimilarMovieResponse: 類似映画レスポンス
    """

    # KVSから類似映画IDを取得
    similar_movie_id_list = kvs_repository.get_similar_movie_id_list(
        movie_id=movie_id,
        model_type=model_type
    )

    # 類似映画を取得
    similar_movie_list = fetch_similar_movies(
        movie_ids=similar_movie_id_list,
        solr_client=solr_client
    )

    return map_similar_movies_response(
        movie_id=movie_id,
        model_type=model_type,
        similar_movie_list=similar_movie_list
    )
