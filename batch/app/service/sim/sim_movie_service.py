from domain.enums.similarity_enums import SimilarityModelType
from infra.client.tmdb.api import AbstractTmdbClient
from infra.repository.sim.redis_repository import AbstarctRedisRepository
from infra.repository.input.movie import AbstractMovieRepository


def exec_construct_tmdb_similarity(
    tmdb_client: AbstractTmdbClient,
    redis_repository: AbstarctRedisRepository,
    movie_repository: AbstractMovieRepository
):
    
    # 出力対象の映画IDを取得
    movie_id_set = set(movie_repository.fetch_all_movie_id())

    # 映画IDごとにKVSデータを構築
    for movie_id in movie_id_set:

        # 類似映画リストを取得
        similar_movie_list = tmdb_client.fetch_similar_movie_list(movie_id=movie_id)
        if not similar_movie_list:
            continue

        # ベスト5のIDを取得
        best_5 = [movie.id for movie in similar_movie_list.results if movie.id in movie_id_set][:5]

        # KVSデータを構築
        redis_repository.save_movie_similarity(
            movie_id=movie_id,
            similar_movies=best_5,
            model_type=SimilarityModelType.TMDB_SIM
        )
