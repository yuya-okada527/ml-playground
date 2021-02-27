"""入稿ロジックモジュール

入稿バッチに関するロジック関数を記述するモジュール
"""


from domain.models.internal.movie_model import Genre
from domain.models.rest.tmdb_model import TmdbMovieGenre


def map_genre_list(
    registered_genre_id_set: set[int],
    english_genres: list[TmdbMovieGenre],
    japanese_genres: list[TmdbMovieGenre],
    force_update: bool
) -> list[Genre]:
    """登録対象の映画ジャンルリストにマッピングを行う

    Args:
        registered_genre_id_set: 登録済ジャンルIDセット
        english_genres: 英語ジャンルリスト
        japanese_genres: 日本語ジャンルリスト
        force_update: 強制アップデートフラグ
    """

    # ジャンルIDで集計
    genre_id_dict = {genre.id: genre for genre in english_genres}

    # ジャンルモデルに詰め替える
    genre_list = []
    for jp_genre in japanese_genres:

        # 登録済のジャンルはスキップ(強制アップデートフラグありの場合は登録する)
        if jp_genre.id in registered_genre_id_set and not force_update:
            continue

        # 日本語表記と英語表記が一致しない場合はスキップ
        en_genre = genre_id_dict.get(jp_genre.id)
        if not en_genre:
            continue

        genre_list.append(Genre(
            genre_id=en_genre.id,
            name=en_genre.name,
            japanese_name=jp_genre.name)
        )

    return genre_list
