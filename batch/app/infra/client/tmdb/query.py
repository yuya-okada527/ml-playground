from typing import Optional

from pydantic import BaseModel


class TmdbQuery(BaseModel):
    api_key: str
    language: Optional[str] = None


class PopularMovieQuery(TmdbQuery):
    page: Optional[int] = None
    region: Optional[str] = None


class MovieGenreQuery(TmdbQuery):
    pass


class MovieDetailQuery(TmdbQuery):
    append_to_response: Optional[str]