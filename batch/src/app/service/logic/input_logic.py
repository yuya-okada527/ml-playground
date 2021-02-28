"""入稿ロジックモジュール

入稿バッチに関するロジック関数を記述するモジュール
"""

from core.logger import create_logger
from domain.models.internal.movie_model import Genre, Review
from domain.models.rest.tmdb_model import TmdbMovieGenre, TmdbMovieReview
from infra.client.tmdb.tmdb_api import AbstractTmdbClient
from infra.repository.input.movie_repository import AbstractMovieRepository
from infra.repository.input.review_repository import AbstractReviewRepository

# 最大類似映画数
MAX_SIMILAR_MOVIES = 5
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


def update_similar_movies_data(
    registered_movies_id_set: set[int],
    registered_similar_movie_map: dict[int, list[int]],
    tmdb_client: AbstractTmdbClient,
    movie_repository: AbstractMovieRepository
) -> int:
    """類似映画データを更新する

    Args:
        registered_movies_id_set (set[int]): 登録済映画IDセット
        registered_similar_movie_map (dict[int, list[int]]): 登録済類似映画データ
        tmdb_client (AbstractTmdbClient): TMDBクライアント
        movie_repository (AbstractMovieRepository): 映画リポジトリ

    Returns:
        int: 更新数
    """

    # 映画IDごとに全ての類似映画を取得
    # TODO パフォーマンス改善
    count = 0
    for i, movie_id in enumerate(registered_movies_id_set, start=1):

        if i % LOG_FREQUENCY == 0:
            log.info(f"{i}件目の処理を実行中.")

        # 登録している映画はスキップする
        if movie_id in registered_similar_movie_map:
            continue

        # 最終ページまで全ての類似映画を取得する
        similar_movie_list = _fetch_similar_movies(
            movie_id=movie_id,
            registered_movies_id_set=registered_movies_id_set,
            tmdb_client=tmdb_client
        )

        # 登録できる映画IDがない場合、スキップ
        if not similar_movie_list:
            continue

        # UPSERT処理で登録
        count += movie_repository.save_similar_movie_list(
            movie_id=movie_id,
            similar_movie_list=similar_movie_list
        )

    return count


def _fetch_similar_movies(
    movie_id: int,
    registered_movies_id_set: set[int],
    tmdb_client: AbstractTmdbClient
) -> list[int]:
    """類似映画リストを取得する

    Args:
        movie_id (int): 映画ID
        registered_movies_id_set (set[int]): 登録済映画IDセット
        tmdb_client (AbstractTmdbClient): TMDBクライアント

    Returns:
        list[int]: 類似映画リスト
    """

    # 最終ページまで全ての類似映画を取得する
    similar_movie_list = []
    current_page = 1
    while True:
        # 類似映画IDリストを更新
        similar_movies_response = tmdb_client.fetch_similar_movie_list(
            movie_id=movie_id,
            page=current_page
        )
        similar_movie_list.extend(
            [movie.id for movie in similar_movies_response.results if movie.id in registered_movies_id_set]
        )

        # 最終ページなら終了
        if current_page == similar_movies_response.total_pages:
            break

        # 類似映画の数が閾値を超えたら打ち切り
        if len(similar_movie_list) >= MAX_SIMILAR_MOVIES:
            break

        # ページを更新し、再度API実行
        current_page += 1

    return similar_movie_list


def _map_review_model(movie_review: TmdbMovieReview, movie_id: int) -> Review:
    """レビューモデルをマッピングする."""
    return Review(
        review_id=movie_review.id,
        movie_id=movie_id,
        review=movie_review.content
    )
