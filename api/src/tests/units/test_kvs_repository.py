import json

import fakeredis
from domain.enums.similarity_enums import SimilarityModelType
from infra.repository.kvs_repository import RedisRepository, _make_sim_key


def test_make_sim_key():

    # テストデータ
    movie_id = 0
    model_type = SimilarityModelType.TMDB_SIM

    # 検証
    assert _make_sim_key(movie_id, model_type) == "0_tmdb-sim"


def test_get_similar_movie_id_list():

    # テストデータ
    movie_id = 0
    model_type = SimilarityModelType.TMDB_SIM
    similar_movies = [1, 2]
    fake_redis_client = fakeredis.FakeRedis()
    fake_redis_client.set("0_tmdb-sim", json.dumps(similar_movies))

    # リポジトリの初期化
    redis_repository = RedisRepository(fake_redis_client)

    # 検証
    actual = redis_repository.get_similar_movie_id_list(
        movie_id=movie_id,
        model_type=model_type
    )

    assert actual == similar_movies
