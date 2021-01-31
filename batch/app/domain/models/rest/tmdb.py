from pydantic import BaseModel


class MovieGenre(BaseModel):
    id: int
    name: str


class MovieGenreList(BaseModel):
    genres: list[MovieGenre]


