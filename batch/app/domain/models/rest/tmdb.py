from typing import Optional
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


class TmdbSimilarMovieList(BaseModel):
    page: int
    results: list[TmdbMovie]
