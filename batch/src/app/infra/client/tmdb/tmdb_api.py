"""TMDB APIクライアントモジュール

TMDBに対するHTTP通信を抽象化するモジュール
"""
from typing import Optional, Protocol

from core.config import TmdbSettings
from domain.enums.movie_enums import MovieLanguage
from domain.models.rest.tmdb_model import (TmdbMovieDetail, TmdbMovieGenreList,
                                           TmdbMovieReviewList,
                                           TmdbPopularMovieList,
                                           TmdbSimilarMovieList)
from infra.client.tmdb.tmdb_query import (MovieDetailQuery, MovieGenreQuery,
                                          MovieReviewQuery, PopularMovieQuery,
                                          SimilarMovieQuery)
from util.http_util import call_get_api

# TMDb APIパス定義
POPULAR_MOVIE_PATH = "/movie/popular"
MOVIE_GENRE_LIST_PATH = "/genre/movie/list"
MOVIE_DETAIL_PATH = "/movie/{movie_id}"
SIMILAR_MOVIE_PATH = "/movie/{movie_id}/similar"
MOVIE_REVIEW_PATH = "/movie/{movie_id}/reviews"


class AbstractTmdbClient(Protocol):

    def fetch_genres(self, language: MovieLanguage) -> TmdbMovieGenreList:
        """ジャンルリスト取得関数

        TMDBから映画ジャンルを取得する.

        Args:
            language: 取得言語
        """
        ...

    def fetch_popular_movies(
        self,
        page: int,
        region: Optional[str] = None,
        language: Optional[MovieLanguage] = None
    ) -> TmdbPopularMovieList:
        """人気映画リスト取得関数

        TMDBから人気映画リストを取得します.

        Args:
            page: 取得ページ
            region: 取得地域
            language: 取得言語
        """
        ...

    def fetch_movie_detail(
        self,
        movie_id: int,
        language: Optional[MovieLanguage] = None,
        append_to_response: Optional[str] = None
    ) -> TmdbMovieDetail:
        """映画詳細取得関数

        TMDBから映画詳細を取得します.

        Args:
            movie_id: 映画ID
            language: 取得言語
            append_to_response: 追加レスポンス項目
        """
        ...

    def fetch_movie_detail_list(
        self,
        movie_id_list: list[int],
        language: Optional[MovieLanguage] = None,
        append_to_response: Optional[str] = None
    ) -> list[TmdbMovieDetail]:
        """映画詳細リスト取得関数

        TMDBから映画詳細リストを取得します.

        Args:
            movie_id_list: 映画IDリスト
            language: 取得言語
            append_to_response: 追加レスポンス項目
        """
        ...

    def fetch_similar_movie_list(
        self,
        movie_id: int,
        language: MovieLanguage = MovieLanguage.EN,
        page: int = 1
    ) -> TmdbSimilarMovieList:
        """類似映画リスト取得関数

        TMDBから類似映画リストを取得する.

        Args:
            movie_id: 映画ID
            language: 取得言語
            page: 取得ページ
        """
        ...

    def fetch_movie_reviews(
        self,
        movie_id: int,
        language: MovieLanguage = MovieLanguage.EN,
        page: int = 1
    ) -> TmdbMovieReviewList:
        """映画レビュー取得関数

        TMDBから映画レビューを取得する.

        Args:
            movie_id: 映画ID
            language: 取得言語
            page: 取得ページ
        """
        ...


class TmdbClient:

    def __init__(self, settings: TmdbSettings) -> None:
        self.base_url = settings.tmdb_url
        self.api_key = settings.tmdb_api_key

    def fetch_genres(self, language: MovieLanguage) -> TmdbMovieGenreList:

        # リクエスト条件を構築
        url = self.base_url + MOVIE_GENRE_LIST_PATH
        query = MovieGenreQuery(
            api_key=self.api_key,
            language=language.value if language else None
        )

        # GETメソッドでAPIを実行
        response = call_get_api(url, query)

        return TmdbMovieGenreList(**response.json())

    def fetch_popular_movies(
        self,
        page: int,
        region: Optional[str] = None,
        language: Optional[MovieLanguage] = None
    ) -> TmdbPopularMovieList:

        # リクエスト条件を構築
        url = self.base_url + POPULAR_MOVIE_PATH
        query = PopularMovieQuery(
            api_key=self.api_key,
            language=language.value if language else None,
            page=page,
            region=region
        )

        # GETメソッドでAPIを実行
        response = call_get_api(url, query)

        return TmdbPopularMovieList(**response.json())

    def fetch_movie_detail(
        self,
        movie_id: int,
        language: Optional[MovieLanguage] = None,
        append_to_response: Optional[str] = None
    ) -> TmdbMovieDetail:

        # リクエスト条件を構築
        url = self.base_url + MOVIE_DETAIL_PATH.format(movie_id=movie_id)
        query = MovieDetailQuery(
            api_key=self.api_key,
            language=language.value if language else None,
            append_to_response=append_to_response
        )

        # GETメソッドでAPIを実行
        response = call_get_api(url, query)

        return TmdbMovieDetail(**response.json())

    def fetch_movie_detail_list(
        self,
        movie_id_list: list[int],
        language: Optional[MovieLanguage] = None,
        append_to_response: Optional[str] = None
    ) -> list[TmdbMovieDetail]:

        movie_detail_list = []
        for movie_id in movie_id_list:
            movie_detail_list.append(self.fetch_movie_detail(
                movie_id=movie_id,
                language=language,
                append_to_response=append_to_response
            ))

        return movie_detail_list

    def fetch_similar_movie_list(
        self,
        movie_id: int,
        language: MovieLanguage = MovieLanguage.EN,
        page: int = 1
    ) -> TmdbSimilarMovieList:

        # リクエスト条件を構築
        url = self.base_url + SIMILAR_MOVIE_PATH.format(movie_id=movie_id)
        query = SimilarMovieQuery(
            api_key=self.api_key,
            language=language.value if language else None,
            page=page
        )

        # GETメソッドでAPIを実行
        response = call_get_api(url=url, query=query)

        return TmdbSimilarMovieList(**response.json())

    def fetch_movie_reviews(
        self,
        movie_id: int,
        language: MovieLanguage = MovieLanguage.EN,
        page: int = 1
    ) -> TmdbMovieReviewList:

        # リクエスト条件を構築
        url = self.base_url + MOVIE_REVIEW_PATH.format(movie_id=movie_id)
        query = MovieReviewQuery(
            api_key=self.api_key,
            language=language.value if language else None,
            page=page
        )

        # GETメソッドでAPIを実行
        response = call_get_api(url=url, query=query)

        return TmdbMovieReviewList(**response.json())
