from typing import Protocol
from core.config import TmdbSettings
from domain.models.rest.tmdb import TmdbMovieGenreList
from infra.client.tmdb.query import (
    MovieGenreQuery
)
from util.http import call_get_api


# TMDb APIパス定義
POPULAR_MOVIE_PATH = "/movie/popular"
MOVIE_GENRE_LIST_PATH = "/genre/movie/list"


class AbstractTmdbClient(Protocol):
    
    def fetch_genres(self, language: str) -> TmdbMovieGenreList:
        ...


class TmdbClient:

    def __init__(self, settings: TmdbSettings) -> None:
        self.base_url = settings.tmdb_url
        self.api_key = settings.tmdb_api_key

    def fetch_genres(self, language: str) -> TmdbMovieGenreList:
        url = self.base_url + MOVIE_GENRE_LIST_PATH
        query = MovieGenreQuery(
            api_key=self.api_key,
            language=language
        )

        # TODO リポジトリパターンで実装するように変更する？
        response = call_get_api(url, query)

        return TmdbMovieGenreList(**response.json())
