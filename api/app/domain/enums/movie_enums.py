"""映画Enumモジュール

映画ドメインに関する区分値を定義するモジュール
"""
from enum import Enum


class MovieField(Enum):
    """Solrのフィールド名を定義する"""
    MOVIE_ID = "movie_id"
    FREE_WORD = "free_word"
    ORIGINAL_TITLE = "original_title"
    JAPANESE_TITLE = "japanese_title"
    OVERVIEW = "overview"
    TAGLINE = "tagline"
    POSTER_PATH = "poster_path"
    BACKDROP_PATH = "backdroppath"
    POPULARITY = "popularity"
    VOTE_AVERAGE = "vote_average"
    RELEASE_DATE = "release_date"
    RELEASE_YEAR = "release_year"
    GENRES = "genres"
    GENRE_LABELS = "genre_labels"
    KEYWORDS = "keywords"
    KEYWORD_LABELS = "keyword_labels"
    INDEX_TIME = "index_time"
    SCORE = "score"
