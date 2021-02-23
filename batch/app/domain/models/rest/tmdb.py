from datetime import datetime
from typing import Optional

from domain.models.internal.movie import RELEASE_DATE_FMT, Genre, Movie
from pydantic import BaseModel


class TmdbMovieGenre(BaseModel):
    id: int
    name: str


class TmdbMovieGenreList(BaseModel):
    genres: list[TmdbMovieGenre]


class TmdbMovie(BaseModel):
    poster_path: Optional[str]
    adult: bool
    overview: str
    release_date: Optional[str]
    genre_ids: list[int]
    id: int
    original_title: str
    original_language: str
    title: str
    backdrop_path: Optional[str]
    popularity: float
    vote_count: int
    video: bool
    vote_average: float


class TmdbPopularMovieList(BaseModel):
    pages: Optional[int]
    results: list[TmdbMovie]
    total_results: int
    total_pages: int


class TmdbProductionCompany(BaseModel):
    name: str
    id: int
    logo_path: Optional[str]
    origin_country: str


class TmdbProductionCountry(BaseModel):
    iso_3166_1: str
    name: str


class TmdbSpokenLanguage(BaseModel):
    iso_639_1: str
    name: str


class TmdbMovieDetail(BaseModel):
    adult: bool
    backdrop_path: Optional[str]
    belongs_to_collection: Optional[dict]
    budget: int
    genres: list[TmdbMovieGenre]
    homepage: Optional[str]
    id: int
    imdb_id: Optional[str]
    original_language: str
    original_title: str
    overview: Optional[str]
    popularity: float
    poster_path: Optional[str]
    production_companies: list[TmdbProductionCompany]
    production_countries: list[TmdbProductionCountry]
    release_date: str
    revenue: int
    runtime: Optional[int]
    spoken_languages: list[TmdbSpokenLanguage]
    status: str
    tagline: Optional[str]
    title: str
    video: bool
    vote_average: float
    vote_count: int

    def to_internal_movie(self) -> Movie:
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
    page: int
    results: list[TmdbMovie]
    total_pages: int
    total_results: int


class TmdbReviewAuthorDetail(BaseModel):
    name: str
    username: str
    avatar_path: Optional[str] = None
    rating: Optional[int] = None


class TmdbMovieReview(BaseModel):
    author: str
    author_details: TmdbReviewAuthorDetail
    content: str
    created_at: str
    id: str
    updated_at: str
    url: str


class TmdbMovieReviewList(BaseModel):
    id: int
    page: int
    results: list[TmdbMovieReview]
    total_pages: int
    total_results: int
