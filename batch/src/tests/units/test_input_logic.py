
from domain.models.internal.movie_model import Genre
from domain.models.rest.tmdb_model import TmdbMovieGenre
from service.logic.input_logic import (map_genre_list, update_review_data,
                                       update_similar_movies_data)
from tests.utils import (FakeMoviewRepository, FakeReviewRepositry,
                         FakeTmdbClient)


def test_map_genre_list_registered_id_is_not_target():

    # テストデータ
    registered_genre_id_set = {0, 1}
    english_genres = [TmdbMovieGenre(id=0, name="name")]
    japanese_genres = [TmdbMovieGenre(id=0, name="名前")]
    force_update = False

    # 検証
    actual = map_genre_list(
        registered_genre_id_set,
        english_genres,
        japanese_genres,
        force_update
    )
    expected = []

    assert actual == expected


def test_map_genre_list_registered_id_is_target_if_force_update():

    # テストデータ
    registered_genre_id_set = {0, 1}
    english_genres = [TmdbMovieGenre(id=0, name="name")]
    japanese_genres = [TmdbMovieGenre(id=0, name="名前")]
    force_update = True

    # 検証
    actual = map_genre_list(
        registered_genre_id_set,
        english_genres,
        japanese_genres,
        force_update
    )
    expected = [Genre(genre_id=0, name="name", japanese_name="名前")]

    assert actual == expected


def test_map_genre_list_mismatched_genre_is_not_target():

    # テストデータ
    registered_genre_id_set = {0, 1}
    english_genres = [TmdbMovieGenre(id=0, name="name")]
    japanese_genres = [TmdbMovieGenre(id=1, name="名前")]
    force_update = False

    # 検証
    actual = map_genre_list(
        registered_genre_id_set,
        english_genres,
        japanese_genres,
        force_update
    )
    expected = []

    assert actual == expected


def test_update_review_data():

    # テストデータ
    registered_movie_ids = [0]
    registered_review_ids = []
    tmdb_client = FakeTmdbClient()
    review_repository = FakeReviewRepositry()

    # 検証
    actual = update_review_data(
        registered_movie_ids=registered_movie_ids,
        registered_review_ids=registered_review_ids,
        tmdb_client=tmdb_client,
        review_repository=review_repository
    )

    assert actual == 2


def test_update_review_data_registered_review_id_is_not_target():

    # テストデータ
    registered_movie_ids = [0]
    registered_review_ids = ["review1"]
    tmdb_client = FakeTmdbClient()
    review_repository = FakeReviewRepositry()

    # 検証
    actual = update_review_data(
        registered_movie_ids=registered_movie_ids,
        registered_review_ids=registered_review_ids,
        tmdb_client=tmdb_client,
        review_repository=review_repository
    )

    assert actual == 1


def test_update_similar_movies_data():

    # テストデータ
    registered_movies_id_set = {0, 2, 3}
    registered_similar_movie_map = {}
    tmdb_client = FakeTmdbClient()
    movie_repository = FakeMoviewRepository()

    # 検証
    actual = update_similar_movies_data(
        registered_movies_id_set=registered_movies_id_set,
        registered_similar_movie_map=registered_similar_movie_map,
        tmdb_client=tmdb_client,
        movie_repository=movie_repository
    )

    assert actual == 2


def test_update_similar_movies_data_registered_movie_is_not_target():

    # テストデータ
    registered_movies_id_set = {0, 2, 3}
    registered_similar_movie_map = {0: []}
    tmdb_client = FakeTmdbClient()
    movie_repository = FakeMoviewRepository()

    # 検証
    actual = update_similar_movies_data(
        registered_movies_id_set=registered_movies_id_set,
        registered_similar_movie_map=registered_similar_movie_map,
        tmdb_client=tmdb_client,
        movie_repository=movie_repository
    )

    assert actual == 0


def test_update_similar_movies_data_registered_movie_is_not_target_similar_movie():

    # テストデータ
    registered_movies_id_set = {0, 3}
    registered_similar_movie_map = {}
    tmdb_client = FakeTmdbClient()
    movie_repository = FakeMoviewRepository()

    # 検証
    actual = update_similar_movies_data(
        registered_movies_id_set=registered_movies_id_set,
        registered_similar_movie_map=registered_similar_movie_map,
        tmdb_client=tmdb_client,
        movie_repository=movie_repository
    )

    assert actual == 1
