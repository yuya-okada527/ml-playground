"""Redisリポジトリモジュール

Redisに対するアクセス機能を提供するモジュール
"""
import json
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
    ) -> int:
        """映画類似度データを保存する.

        Args:
            movie_id: 映画ID
            similar_movies: 類似映画IDリスト
            model_type: 類似度判定モデルタイプ
        """
        ...


class RedisRepository:

    def __init__(self, redis_client: redis.Redis = REDIS_CLIENT) -> None:
        self.redis_client = redis_client

    def save_movie_similarity(
        self,
        movie_id: int,
        similar_movies: list[int],
        model_type: SimilarityModelType
    ) -> int:
        # ガード
        assert model_type is not None

        # キーを作成
        key = _make_sim_key(movie_id, model_type)

        # 類似映画を保存
        self.redis_client.set(key, json.dumps(similar_movies))

        return len(similar_movies)


def _make_sim_key(movie_id: int, model_type: SimilarityModelType) -> str:
    return f"{movie_id}_{model_type.value}"
