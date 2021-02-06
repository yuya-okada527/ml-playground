from enum import Enum


class MovieField(Enum):
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
    GENRES = "genres"
    GENRE_LABELS = "genre_labels"
    KEYWORDS = "keywords"
    KEYWORD_LABELS = "keyword_labels"
    INDEX_TIME = "index_time"
    SCORE = "score"
