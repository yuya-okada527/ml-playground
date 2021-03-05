from service.logic.similarity_logic import save_tmdb_similarity_data
from tests.utils import FakeRedisRepository


def test_save_tmdb_similarity_data():

    # テストデータ
    similar_movies_map = {
        0: [1, 2, 3, 4, 5, 6, 7],
        1: [1, 2, 3],
        2: []
    }
    redis_repository = FakeRedisRepository()

    # 検証
    actual = save_tmdb_similarity_data(
        similar_movies_map=similar_movies_map,
        redis_repository=redis_repository
    )

    assert actual == 8
