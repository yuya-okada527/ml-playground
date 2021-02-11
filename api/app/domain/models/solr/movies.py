from typing import List, Dict, Optional

from pydantic import BaseModel


class SolrResponseHeaderModel(BaseModel):
    status: int
    QTime: int
    params: Dict[str, str]


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
    release_date: Optional[str] = None
    release_year: Optional[int] = None
    genres: List[int] = []
    genre_labels: List[str] = []
    keywords: List[int] = []
    keyword_labels: List[str] = []


class SolrResponseModel(BaseModel):
    numFound: int
    start: int
    numFoundExact: bool
    docs: List[MovieSolrModel]


class SolrResultModel(BaseModel):
    responseHeader: SolrResponseHeaderModel
    response: SolrResponseModel