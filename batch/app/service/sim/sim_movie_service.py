from core.decorator import service
from core.logging import create_logger
from domain.enums.similarity_enums import SimilarityModelType
from infra.client.tmdb.api import AbstractTmdbClient
from infra.repository.sim.redis_repository import AbstarctRedisRepository
from infra.repository.input.movie import AbstractMovieRepository

log = create_logger(__file__)


@service
def exec_construct_tmdb_similarity(
    redis_repository: AbstarctRedisRepository,
    movie_repository: AbstractMovieRepository
) -> None:

    log.info("TMDB-API類似映画データ構築処理実行開始.")

    # 類似映画情報を全て取得
    similar_movies_map = movie_repository.fetch_all_similar_movie()

    # 映画IDごとにKVSデータを構築
    for movie_id, similar_movies in similar_movies_map.items():
        # ベスト5のIDを取得
        best_5 = similar_movies[:5]

        # KVSデータを構築
        redis_repository.save_movie_similarity(
            movie_id=movie_id,
            similar_movies=best_5,
            model_type=SimilarityModelType.TMDB_SIM
        )

    log.info("TMDB-API類似映画データ構築処理実行終了.")
