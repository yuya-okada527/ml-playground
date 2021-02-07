from entrypoints.v1.movie.messages.movie_messages import SimilarMovieResponse
from domain.enums.similarity_enums import SimilarityModelType
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

    print(similar_movie_id_list)


    return None
