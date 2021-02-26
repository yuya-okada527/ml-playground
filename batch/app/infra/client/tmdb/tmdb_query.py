"""TMDBクエリモジュール

TMDBに対するクエリを記述するモジュール
"""
from typing import Optional

from pydantic import BaseModel


class TmdbQuery(BaseModel):
    """TMDBクエリ"""
    api_key: str
    language: Optional[str] = None


class PopularMovieQuery(TmdbQuery):
    """人気映画クエリ"""
    page: Optional[int] = None
    region: Optional[str] = None


class MovieGenreQuery(TmdbQuery):
    """映画ジャンルクエリ"""
    pass


class MovieDetailQuery(TmdbQuery):
    """映画詳細クエリ"""
    append_to_response: Optional[str]


class SimilarMovieQuery(TmdbQuery):
    """類似映画クエリ"""
    page: Optional[int]


class MovieReviewQuery(TmdbQuery):
    """映画レビュークエリ"""
    page: Optional[int]
