from datetime import date

from domain.models.internal.movie_model import Genre, Movie
from domain.models.rest.tmdb_model import (TmdbMovieDetail, TmdbMovieGenre,
                                           TmdbProductionCompany,
                                           TmdbProductionCountry,
                                           TmdbSpokenLanguage)


def test_tmdb_movie_detail_mapping():

    # テストデータ
    movie_detail = TmdbMovieDetail(
        adult=False,
        budget=0,
        genres=[TmdbMovieGenre(id=0, name="name")],
        id=0,
        original_language="ja",
        original_title="original_title",
        popularity=0.1,
        production_companies=[TmdbProductionCompany(name="name", id=0, origin_country="ja")],
        production_countries=[TmdbProductionCountry(iso_3166_1="ja", name="japan")],
        release_date="2020-01-01",
        revenue=0,
        spoken_languages=[TmdbSpokenLanguage(iso_639_1="ja", name="japanese")],
        status="status",
        title="title",
        video=True,
        vote_average=0.1,
        vote_count=0
    )

    expected = Movie(
        movie_id=0,
        original_title="original_title",
        japanese_title="title",
        popularity=0.1,
        vote_average=0.1,
        vote_count=0,
        release_date=date(2020, 1, 1),
        genres=[Genre(genre_id=0)]
    )

    assert movie_detail.to_internal_movie() == expected
