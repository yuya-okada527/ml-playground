from pydantic import BaseModel


class TmdbMovieGenre(BaseModel):
    id: int
    name: str


class TmdbMovieGenreList(BaseModel):
    genres: list[TmdbMovieGenre]


