"""類似データサービスモジュール

類似データ構築バッチに関するサービス関数を記述するモジュール
"""
from core.aop import batch_service
from core.logger import create_logger
from domain.enums.similarity_enums import SimilarityModelType
from infra.repository.input.movie_repository import AbstractMovieRepository
from infra.repository.similarity.redis_repository import \
    AbstarctRedisRepository

log = create_logger(__file__)


@batch_service
def exec_construct_tmdb_similarity(
    redis_repository: AbstarctRedisRepository,
    movie_repository: AbstractMovieRepository
) -> None:
    """TMDB APIに基づく類似度データを構築する処理を実行します.

    Args:
        redis_repository (AbstarctRedisRepository): Redisリポジトリ
        movie_repository (AbstractMovieRepository): 映画リポジトリ
    """

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
