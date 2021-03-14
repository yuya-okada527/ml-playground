"""映画APIメッセージモジュール

映画APIに対するIFメッセージを記述するモジュール
"""
from typing import List, Optional

from domain.enums.similarity_enums import SimilarityModelType
from pydantic import BaseModel, Field


class MovieResponse(BaseModel):
    """映画レスポンス"""
    movie_id: int = Field(..., description="MovieRecommender共通映画ID")
    original_title: str = Field(..., description="オリジナルの映画タイトル")
    japanese_title: str = Field(..., description="日本語タイトル")
    overview: Optional[str] = Field(None, description="シナリオ")
    tagline: Optional[str] = Field(None, description="キャッチコピー")
    poster_url: str = Field(..., description="ポスター画像へのパス")
    backdrop_url: Optional[str] = Field(None, description="背景画像へのパス")
    popularity: float = Field(..., description="人気スコア")
    vote_average: float = Field(..., description="投票平均点")
    release_date: Optional[str] = Field(None, description="公開日")
    release_year: Optional[int] = Field(None, description="公開年")
    genre_labels: List[str] = Field(..., description="ジャンル名")
    genres: List[int] = Field(..., description="ジャンルID")


class SearchMovieResponse(BaseModel):
    """映画検索レスポンス"""
    start: int = Field(..., description="取得開始位置(0始まり)")
    returned_num: int = Field(..., description="実際に返却するリストの数を返します.")
    available_num: int = Field(..., description="検索条件にヒットした件数を返します.")
    results: List[MovieResponse] = Field(..., description="検索結果リスト")


class SimilarMovieResponse(BaseModel):
    """類似映画レスポンス"""
    target_id: int = Field(..., description="類似検索対象映画ID")
    model_type: SimilarityModelType = Field(..., description="類似性判定モデル")
    results: List[MovieResponse] = Field(..., description="類似映画リスト")


class MovieIdResponse(BaseModel):
    """映画IDレスポンス"""
    movie_ids: List[int] = Field(..., description="映画IDリスト")
