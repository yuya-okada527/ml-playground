from service.similarity_service import exec_construct_tmdb_similarity
from tests.utils import FakeMoviewRepository, FakeRedisRepository


def test_exec_construct_tmdb_similarity():

    # 例外が出ないことを検証
    exec_construct_tmdb_similarity(
        redis_repository=FakeRedisRepository(),
        movie_repository=FakeMoviewRepository()
    )
