from typing import Protocol, Optional

from core.config import TmdbSettings
from domain.models.rest.tmdb import TmdbMovieDetail, TmdbMovieGenreList, TmdbPopularMovieList
from infra.client.tmdb.query import (
    MovieDetailQuery, MovieGenreQuery, PopularMovieQuery
)
from util.http import call_get_api


# TMDb APIパス定義
POPULAR_MOVIE_PATH = "/movie/popular"
MOVIE_GENRE_LIST_PATH = "/genre/movie/list"
MOVIE_DETAIL_PATH = "/movie/{movie_id}"


class AbstractTmdbClient(Protocol):
    
    def fetch_genres(self, language: str) -> TmdbMovieGenreList:
        ...
    
    def fetch_popular_movies(
        self, 
        page: int, 
        region: Optional[str], 
        language: Optional[str] = None
    ) -> TmdbPopularMovieList:
        ...
    
    def fetch_movie_detail(
        self, 
        movie_id: int, 
        language: Optional[str] = None, 
        append_to_response: Optional[str] = None
    ) -> TmdbMovieDetail:
        ...
    
    def fetch_movie_detail_list(
        self,
        movie_id_list: list[int],
        language: Optional[str] = None,
        append_to_response: Optional[str] = None
    ) -> list[TmdbMovieDetail]:
        ...


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
    
    def fetch_movie_detail(
        self, 
        movie_id: int, 
        language: Optional[str] = None, 
        append_to_response: Optional[str] = None
    ) -> TmdbMovieDetail:
        
        # リクエスト条件を構築
        url = self.base_url + MOVIE_DETAIL_PATH.format(movie_id=movie_id)
        query = MovieDetailQuery(
            api_key=self.api_key,
            language=language,
            append_to_response=append_to_response
        )

        # GETメソッドでAPIを実行
        response = call_get_api(url, query)

        return TmdbMovieDetail(**response.json())

    def fetch_movie_detail_list(
        self,
        movie_id_list: list[int],
        language: Optional[str] = None,
        append_to_response: Optional[str] = None
    ) -> list[TmdbMovieDetail]:
        
        movie_detail_list = []
        for movie_id in movie_id_list:
            movie_detail_list.append(self.fetch_movie_detail(
                movie_id=movie_id,
                language=language,
                append_to_response=append_to_response
            ))

            print(movie_id)
        
        return movie_detail_list