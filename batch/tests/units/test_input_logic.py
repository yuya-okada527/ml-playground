from domain.models.internal.movie_model import Genre
from domain.models.rest.tmdb_model import TmdbMovieGenre
from service.logic.input_logic import map_genre_list


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
