"""KVSリポジトリモジュール

KVS(Key Value Store)に対するアクセス機能を提供するモジュール
"""
import json
from typing import List, Protocol

import redis
from core.config import RedisSettings
from domain.enums.similarity_enums import SimilarityModelType

REDIS_SETTINGS = RedisSettings()
REDIS_CLIENT = redis.Redis(host=REDIS_SETTINGS.redis_host, port=REDIS_SETTINGS.redis_port)


class AbstractKvsRepository(Protocol):

    def get_similar_movie_id_list(
        self,
        movie_id: int,
        model_type: SimilarityModelType
    ) -> List[int]:
        """類似映画IDリストを取得する

        Args:
            movie_id (int): 映画ID
            model_type (SimilarityModelType): 類似映画判定モデル

        Returns:
            List[int]: 類似映画IDリスト
        """
        ...


class RedisRepository:

    def __init__(self, client: redis.Redis = REDIS_CLIENT) -> None:
        self.client = client

    def get_similar_movie_id_list(
        self,
        movie_id: int,
        model_type: SimilarityModelType
    ) -> List[int]:

        # キー名を作成
        key = _make_sim_key(movie_id=movie_id, model_type=model_type)

        # 類似映画IDを取得
        response: bytes = self.client.get(key)  # type: ignore
        if not response:
            return []

        return json.loads(response.decode("utf-8"))


async def get_kvs_repository() -> AbstractKvsRepository:
    """KVSリポジトリを取得する

    Returns:
        AbstractKvsRepository: KVSリポジトリ
    """
    return RedisRepository()


def _make_sim_key(movie_id: int, model_type: SimilarityModelType) -> str:
    """類似データのキーを作成する

    Args:
        movie_id (int): 映画ID
        model_type (SimilarityModelType): 類似映画判定モデル

    Returns:
        str: キー
    """
    return f"{movie_id}_{model_type.value}"
