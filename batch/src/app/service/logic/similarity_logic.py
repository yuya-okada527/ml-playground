"""類似データロジックモジュール

類似データ作成バッチに関するロジック関数を記述するモジュール
"""
from domain.enums.similarity_enums import SimilarityModelType
from infra.repository.similarity.redis_repository import \
    AbstarctRedisRepository


def save_tmdb_similarity_data(
    similar_movies_map: dict[int, list[int]],
    redis_repository: AbstarctRedisRepository
) -> int:
    """映画IDごとにKVSデータを構築する

    Args:
        similar_movies_map (dict[int, list[int]]): 類似映画データ
        redis_repository (AbstarctRedisRepository): Redisリポジトリ
    """

    # 映画IDごとにKVSデータを構築
    count = 0
    for movie_id, similar_movies in similar_movies_map.items():
        # ベスト5のIDを取得
        best_5 = similar_movies[:5]

        # KVSデータを構築
        count += redis_repository.save_movie_similarity(
            movie_id=movie_id,
            similar_movies=best_5,
            model_type=SimilarityModelType.TMDB_SIM
        )

    return count
