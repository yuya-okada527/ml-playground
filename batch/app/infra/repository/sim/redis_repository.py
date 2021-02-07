from typing import Protocol

import redis

from core.config import RedisSettings
from domain.enums.similarity_enums import SimilarityModelType

REDIS_SETTINGS = RedisSettings()
REDIS_CLIENT = redis.Redis(host=REDIS_SETTINGS.redis_host, port=REDIS_SETTINGS.redis_port)

class AbstarctRedisRepository(Protocol):

    def save_movie_similarity(
        self, 
        movie_id: int, 
        similar_movies: list[int], 
        model_type: SimilarityModelType
    ):
        ...


class RedisRepository:

    def save_movie_similarity(
        self, 
        movie_id: int, 
        similar_movies: list[int], 
        model_type: SimilarityModelType
    ):
        # ガード
        assert model_type is not None

        # キーを作成
        key = _make_sim_key(movie_id, model_type)

        # 類似映画を保存
        REDIS_CLIENT.set(key, similar_movies)


def _make_sim_key(movie_id: int, model_type: SimilarityModelType) -> str:
    return f"{movie_id}_{model_type.value}"