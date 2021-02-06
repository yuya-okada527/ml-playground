from typing import Optional

from pydantic import BaseModel


class SolrResponseHeaderModel(BaseModel):
    status: int
    QTime: int
    params: dict[str, str]


class MovieSolrModel(BaseModel):
    movie_id: str
    original_title: str
    japanese_title: str
    overview: Optional[str] = None
    tagline: Optional[str] = None
    poster_path: str
    backdrop_path: Optional[str] = None
    popularity: float
    vote_average: float
    genres: list[int] = []
    genre_labels: list[str] = []
    keywords: list[int] = []
    keyword_labels: list[str] = []


class SolrResponseModel(BaseModel):
    numFound: int
    start: int
    numFoundExact: bool
    docs: list[MovieSolrModel]


class SolrResultModel(BaseModel):
    responseHeader: SolrResponseHeaderModel
    response: SolrResponseModel