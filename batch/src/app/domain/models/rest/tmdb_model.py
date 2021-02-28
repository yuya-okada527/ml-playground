"""TMDBモデルモジュール

TMDBに関するモデルを記述するモジュール
"""
from datetime import datetime
from typing import Any, Optional

from domain.models.internal.movie_model import RELEASE_DATE_FMT, Genre, Movie
from pydantic import BaseModel


class TmdbMovieGenre(BaseModel):
    """TMDB映画ジャンルモデル"""
    id: int
    name: str


class TmdbMovieGenreList(BaseModel):
    """TMDB映画ジャンルリストモデル"""
    genres: list[TmdbMovieGenre] = []


class TmdbMovie(BaseModel):
    """TMDB映画モデル"""
    poster_path: Optional[str] = None
    adult: bool
    overview: str
    release_date: Optional[str] = None
    genre_ids: list[int] = []
    id: int
    original_title: str
    original_language: str
    title: str
    backdrop_path: Optional[str] = None
    popularity: float
    vote_count: int
    video: bool
    vote_average: float


class TmdbPopularMovieList(BaseModel):
    """人気映画モデルリスト"""
    pages: Optional[int] = None
    results: list[TmdbMovie] = []
    total_results: int
    total_pages: int


class TmdbProductionCompany(BaseModel):
    """TMDB制作会社モデル"""
    name: str
    id: int
    logo_path: Optional[str] = None
    origin_country: str


class TmdbProductionCountry(BaseModel):
    """TMDB制作国家"""
    iso_3166_1: str
    name: str


class TmdbSpokenLanguage(BaseModel):
    """制作映画言語"""
    iso_639_1: str
    name: str


class TmdbMovieDetail(BaseModel):
    """TMDB映画詳細"""
    adult: bool
    backdrop_path: Optional[str] = None
    belongs_to_collection: Optional[dict[str, Any]] = {}
    budget: int
    genres: list[TmdbMovieGenre] = []
    homepage: Optional[str] = None
    id: int
    imdb_id: Optional[str] = None
    original_language: str
    original_title: str
    overview: Optional[str] = None
    popularity: float
    poster_path: Optional[str] = None
    production_companies: list[TmdbProductionCompany] = []
    production_countries: list[TmdbProductionCountry] = []
    release_date: str
    revenue: int
    runtime: Optional[int] = None
    spoken_languages: list[TmdbSpokenLanguage] = []
    status: str
    tagline: Optional[str] = None
    title: str
    video: bool
    vote_average: float
    vote_count: int

    def to_internal_movie(self) -> Movie:
        """内部モデル変換関数"""
        return Movie(
            movie_id=self.id,
            imdb_id=self.imdb_id,
            original_title=self.original_title,
            japanese_title=self.title,
            overview=self.overview,
            tagline=self.tagline,
            poster_path=self.poster_path,
            backdrop_path=self.backdrop_path,
            popularity=self.popularity,
            vote_average=self.vote_average,
            vote_count=self.vote_count,
            release_date=datetime.strptime(self.release_date, RELEASE_DATE_FMT) if self.release_date else None,
            genres=[Genre(genre_id=genre.id) for genre in self.genres]
        )


class TmdbSimilarMovieList(BaseModel):
    """TMDB類似映画リスト"""
    page: int
    results: list[TmdbMovie] = []
    total_pages: int
    total_results: int


class TmdbReviewAuthorDetail(BaseModel):
    """TMDBレビュー者詳細"""
    name: str
    username: str
    avatar_path: Optional[str] = None
    rating: Optional[int] = None


class TmdbMovieReview(BaseModel):
    """TMDB映画レビュー"""
    author: str
    author_details: TmdbReviewAuthorDetail
    content: str
    created_at: str
    id: str
    updated_at: str
    url: str


class TmdbMovieReviewList(BaseModel):
    """TMDB映画レビューリスト"""
    id: int
    page: int
    results: list[TmdbMovieReview] = []
    total_pages: int
    total_results: int
