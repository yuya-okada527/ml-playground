"""入稿ロジックモジュール

入稿バッチに関するロジック関数を記述するモジュール
"""

from core.logger import create_logger
from domain.models.internal.movie_model import Genre, Review
from domain.models.rest.tmdb_model import TmdbMovieGenre, TmdbMovieReview
from infra.client.tmdb.tmdb_api import AbstractTmdbClient
from infra.repository.input.review_repository import AbstractReviewRepository

# ログ頻度
LOG_FREQUENCY = 20


log = create_logger(__file__)


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


def update_review_data(
    registered_movie_ids: list[int],
    registered_review_ids: list[str],
    tmdb_client: AbstractTmdbClient,
    review_repository: AbstractReviewRepository,
) -> int:
    """レビューデータを更新します.

    Args:
        registered_movie_ids: 登録済映画IDリスト
        registered_review_ids: 登録済レビューIDリスト
        tmdb_client: TMDBクライアント
        review_repository: レビューリポジトリ
    """

    # 映画IDごとにレビューデータを取得・登録していく
    count = 0
    for i, movie_id in enumerate(registered_movie_ids, start=1):
        # ページは1固定とする
        movie_review_response = tmdb_client.fetch_movie_reviews(movie_id=movie_id, page=1)
        # 内部モデルに変換
        movie_review_list = [
            _map_review_model(review, movie_id)
            for review in movie_review_response.results
            if review.id not in registered_review_ids  # 登録済の物はスキップする(強制アップデートフラグがあればスキップしない)
        ]

        # 登録
        count += review_repository.save_review_list(movie_review_list)

        if i % LOG_FREQUENCY == 0:
            log.info(f"{i}件目の処理が完了しました.")

    return count


def _map_review_model(movie_review: TmdbMovieReview, movie_id: int) -> Review:
    """レビューモデルをマッピングする."""
    return Review(
        review_id=movie_review.id,
        movie_id=movie_id,
        review=movie_review.content
    )
