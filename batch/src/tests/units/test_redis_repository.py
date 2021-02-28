import json

import fakeredis
from domain.enums.similarity_enums import SimilarityModelType
from infra.repository.similarity.redis_repository import (RedisRepository,
                                                          _make_sim_key)


def test_save_movie_similarity():

    # テストデータ
    movie_id = 0
    similar_movies = [1, 2]
    model_type = SimilarityModelType.TMDB_SIM

    # リポジトリの初期化
    fake_redis_client = fakeredis.FakeStrictRedis()
    redis_repository = RedisRepository(fake_redis_client)

    # 検証
    redis_repository.save_movie_similarity(
        movie_id=movie_id,
        similar_movies=similar_movies,
        model_type=model_type
    )
    key = _make_sim_key(movie_id, model_type)

    assert fake_redis_client.get(key).decode("utf-8") == json.dumps(similar_movies)
