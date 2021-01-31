from typing import Protocol, Optional

from core.config import TmdbSettings
from domain.models.rest.tmdb import TmdbMovieGenreList, TmdbPopularMovieList
from infra.client.tmdb.query import (
    MovieGenreQuery, PopularMovieQuery
)
from util.http import call_get_api


# TMDb APIパス定義
POPULAR_MOVIE_PATH = "/movie/popular"
MOVIE_GENRE_LIST_PATH = "/genre/movie/list"


class AbstractTmdbClient(Protocol):
    
    def fetch_genres(self, language: str) -> TmdbMovieGenreList:
        ...
    
    def fetch_popular_movies(
        self, 
        page: int, 
        region: Optional[str], 
        language: Optional[str] = None
    ) -> TmdbPopularMovieList:
        pass


class TmdbClient:

    def __init__(self, settings: TmdbSettings) -> None:
        self.base_url = settings.tmdb_url
        self.api_key = settings.tmdb_api_key

    def fetch_genres(self, language: str) -> TmdbMovieGenreList:

        # リクエスト条件を構築
        url = self.base_url + MOVIE_GENRE_LIST_PATH
        query = MovieGenreQuery(
            api_key=self.api_key,
            language=language
        )

        # GETメソッドでAPIを実行
        response = call_get_api(url, query)

        return TmdbMovieGenreList(**response.json())

    def fetch_popular_movies(
        self, 
        page: int, 
        region: Optional[str] = None,
        language: Optional[str] = None
    ) -> TmdbPopularMovieList:
        
        # リクエスト条件を構築
        url = self.base_url + POPULAR_MOVIE_PATH
        query = PopularMovieQuery(
            api_key=self.api_key,
            language=language,
            page=page,
            region=region
        )

        # GETメソッドでAPIを実行
        response = call_get_api(url, query)

        return TmdbPopularMovieList(**response.json())
