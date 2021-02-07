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
        ...


class RedisRepository:
    
    def get_similar_movie_id_list(
        self, 
        movie_id: int, 
        model_type: SimilarityModelType
    ) -> List[int]:
        
        # キー名を作成
        key = _make_sim_key(movie_id=movie_id, model_type=model_type)

        # 類似映画IDを取得
        response = REDIS_CLIENT.get(key)
        if not response:
            return []
        
        return json.loads(response.decode("utf-8"))


async def get_kvs_repository() -> AbstractKvsRepository:
    return RedisRepository()


def _make_sim_key(movie_id: int, model_type: SimilarityModelType) -> str:
    return f"{movie_id}_{model_type.value}"
