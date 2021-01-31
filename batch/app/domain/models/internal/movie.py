from pydantic import BaseModel


class Genre(BaseModel):
    genre_id: int
    name: str
    japanese_name: str


class Review(BaseModel):
    review_id: str
    review: str


class Keyword(BaseModel):
    keyword_id: str
    name: str
    japanese_name: str


class Movie(BaseModel):
    movie_id: int
    tmdb_id: str
    imdb_id: str
    original_title: str
    japanese_title: str
    overview: str
    tagline: str
    poster_path: str
    backdrop_path: str
    popularity: float
    vote_average: float
    vote_count: int
    reviews: list[Review] = []
    genres: list[Genre] = []
    keywords: list[Keyword] = []
