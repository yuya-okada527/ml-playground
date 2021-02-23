"""映画モデルモジュール

内部用の映画に関するモデルを記述するモジュール
"""
from datetime import date
from typing import Optional

from pydantic import BaseModel

# 映画公開日付の文字列フォーマット
RELEASE_DATE_FMT = "%Y-%m-%d"


class Genre(BaseModel):
    """ジャンルモデル

    映画ジャンルのドメインモデル

    Attributes:
        genre_id: ジャンルID (TMDBのジャンルIDと一致)
        name: ジャンル英語名
        japanese_name: ジャンル日本語名
    """
    genre_id: int
    name: Optional[str]
    japanese_name: Optional[str]


class Review(BaseModel):
    """レビューモデル

    映画レビューモデル

    Attributes:
        review_id: レビューID (TMDBのレビューIDと一致)
        movie_id: 映画ID
        review: レビュー中身
    """
    review_id: str
    movie_id: int
    review: str


class Keyword(BaseModel):
    """キーワードモデル

    映画キーワードモデル

    Attributes:
        keyword_id: キーワードID
        name: キーワード英語名
        japanese_name: キーワード日本語名
    """
    keyword_id: str
    name: str
    japanese_name: str


class Movie(BaseModel):
    """映画モデル

    映画モデル

    Attributes:
        movie_id: 映画ID (TMDBの映画IDを利用)
        imdb_id: IMDB ID
        original_title: オリジナルタイトル
        japanese_title: 日本語版タイトル
        overview: シナリオ
        tagline: キャッチフレーズ
        poster_path: ポスター画像パス (TMDBの画像配布サーバ)
        backdrop_path: 背景画像パス (TMDBの画像配布サーバ)
        popularity: 人気度
        vote_average: 投票平均 (TMDBの平均レート)
        vote_count: 投票数
        release_date: 公開日
        reviews: レビューリスト
        genres: ジャンルリスト
        keywords: キーワードリスト
    """
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
        """公開日付日付文字列 (%Y-%m-%d)"""
        if self.release_date:
            return date.strftime(self.release_date, RELEASE_DATE_FMT)
        return None

    @property
    def release_year(self) -> Optional[int]:
        """公開年"""
        if self.release_date:
            return self.release_date.year
        return None

    def can_output(self) -> bool:
        """出稿判定

        検索システムにインデックスを構築できるか判定する

        Returns:
            インデックス構築可能ならTrue, 不可能ならFalse
        """

        # シナリオない場合出稿しない
        if not self.overview:
            return False
        # ポスタと背景の両方がない場合出稿しない
        if not self.poster_path and not self.backdrop_path:
            return False
        # TODO 類似映画の数で絞る処理を追加

        return True
