from typing import Optional
from datetime import date

from pydantic import BaseModel


RELEASE_DATE_FMT = "%Y-%m-%d"


class Genre(BaseModel):
    genre_id: int
    name: Optional[str]
    japanese_name: Optional[str]


class Review(BaseModel):
    review_id: str
    movie_id: int
    review: str


class Keyword(BaseModel):
    keyword_id: str
    name: str
    japanese_name: str


class Movie(BaseModel):
    movie_id: str
    imdb_id: Optional[str] = None
    original_title: str
    japanese_title: str
    overview: str
    tagline: str
    poster_path: str
    backdrop_path: Optional[str] = None
    popularity: float
    vote_average: float
    vote_count: int
    release_date: Optional[date] = None
    reviews: list[Review] = []
    genres: list[Genre] = []
    keywords: list[Keyword] = []

    @property
    def release_date_str(self) -> Optional[str]:
        if self.release_date:
            return date.strftime(self.release_date, RELEASE_DATE_FMT)
        return None
    
    @property
    def release_year(self) -> Optional[int]:
        if self.release_date:
            return self.release_date.year
        return None

