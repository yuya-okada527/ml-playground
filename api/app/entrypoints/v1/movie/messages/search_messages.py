from pydantic import BaseModel, Field


class MovieResponse(BaseModel):
    movie_id: int = Field(..., description="MovieRecommender共通映画ID")
    original_title: str = Field(..., description="オリジナルの映画タイトル")
    japanese_title: str = Field(..., description="日本語タイトル")
    overview: str = Field(..., description="シナリオ")
    tagline: str = Field(..., description="キャッチコピー")
    poster_path: str = Field(..., description="ポスター画像へのパス")
    backdrop_path: str = Field(..., description="背景画像へのパス")
    popularity: float = Field(..., description="人気スコア")
    vote_average: float = Field(..., description="投票平均点")
    genre_labels: list[str] = Field(..., description="ジャンル名")
    genres: list[int] = Field(..., description="ジャンルID")


class SearchMovieResponse(BaseModel):
    start: int = Field(..., description="取得開始位置(0始まり)")
    returned_num: int = Field(..., description="実際に返却するリストの数を返します.")
    available_num: int = Field(..., description="検索条件にヒットした件数を返します.")
    results: list[MovieResponse] = Field(..., description="検索結果リスト")
