from typing import Optional
from pydantic import BaseModel


class TmdbMovieGenre(BaseModel):
    id: int
    name: str


class TmdbMovieGenreList(BaseModel):
    genres: list[TmdbMovieGenre]


class TmdbPopularMovie(BaseModel):
    poster_path: Optional[str]
    adult: bool
    overview: str
    release_date: str
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
    results: list[TmdbPopularMovie]
    total_results: int
    total_pages: int
