import pytest
from infra.client.tmdb.tmdb_api import TmdbClient
from service.input_service import (exec_update_genre_master,
                                   exec_update_movie_reviews,
                                   exec_update_popular_movies,
                                   exec_update_similar_movies)
from tests.utils import (FakeGenreRepository, FakeMoviewRepository,
                         FakeReviewRepositry, FakeTmdbClient)


@pytest.mark.parametrize("force_update", [True, False])
def test_exec_update_genre_master(force_update):

    # 例外が発生しないことを検証
    exec_update_genre_master(
        force_update=force_update,
        genre_repository=FakeGenreRepository(),
        tmdb_client=FakeTmdbClient()
    )


@pytest.mark.parametrize("force_update", [True, False])
def test_exec_update_popular_movies(force_update):

    # 例外が発生しないことを検証
    exec_update_popular_movies(
        page=1,
        force_update=force_update,
        tmdb_client=FakeTmdbClient(),
        movie_repository=FakeMoviewRepository()
    )


def test_exec_update_movie_reviews():

    # 例外が発生しないことを検証
    exec_update_movie_reviews(
        tmdb_client=FakeTmdbClient(),
        movie_repository=FakeMoviewRepository(),
        review_repository=FakeReviewRepositry()
    )


def test_exec_update_similar_movies():

    # 例外が発生しないことを検証
    exec_update_similar_movies(
        tmdb_client=FakeTmdbClient(),
        movie_repository=FakeMoviewRepository()
    )
