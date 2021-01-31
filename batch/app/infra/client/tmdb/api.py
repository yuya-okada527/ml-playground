from core.config import TmdbSettings
from domain.models.rest.tmdb import TmdbMovieGenreList
from infra.client.tmdb.query import (
    MovieGenreQuery
)
from util.http import call_get_api


# TMDb APIパス定義
POPULAR_MOVIE_PATH = "/movie/popular"
MOVIE_GENRE_LIST_PATH = "/genre/movie/list"


def fetch_genres(language: str):
    settings = TmdbSettings()
    url = settings.tmdb_url + MOVIE_GENRE_LIST_PATH
    query = MovieGenreQuery(
        api_key=settings.tmdb_api_key,
        language=language
    )

    # TODO リポジトリパターンで実装するように変更する？
    response = call_get_api(url, query)

    return TmdbMovieGenreList(**response.json())

