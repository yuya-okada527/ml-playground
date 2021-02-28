"""Solr映画モデルモジュール

Solr上のmoviesコレクションのスキーマを表すモデルを記述するモジュール
"""
from typing import Optional

from pydantic import BaseModel


class MovieSolrModel(BaseModel):
    """検索用映画モデル"""
    movie_id: str
    free_word: str
    original_title: str
    japanese_title: str
    overview: str
    tagline: str
    poster_path: str
    backdrop_path: Optional[str] = None
    popularity: float
    vote_average: float
    release_date: Optional[str] = None
    release_year: Optional[int] = None
    genres: list[int] = []
    genre_labels: list[str] = []
    keywords: list[int] = []
    keyword_labels: list[str] = []
    index_time: int
