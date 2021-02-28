"""入稿サービスモジュール

入稿バッチに関するサービス関数を記述するモジュール

Todo:
    * ロジックを切り出して、テスタビリティを向上する
    * データストアに対するアクセスは、いったんサービス層で実行
"""
from core.aop import batch_service
from core.logger import create_logger
from domain.enums.movie_enums import MovieLanguage
from infra.client.tmdb.tmdb_api import AbstractTmdbClient
from infra.repository.input.genre_repository import AbstractGenreRepository
from infra.repository.input.movie_repository import AbstractMovieRepository
from infra.repository.input.review_repository import AbstractReviewRepository

from service.logic.input_logic import (map_genre_list, update_review_data,
                                       update_similar_movies_data)

log = create_logger(__file__)


@batch_service
def exec_update_genre_master(
    force_update: bool,
    genre_repository: AbstractGenreRepository,
    tmdb_client: AbstractTmdbClient
) -> None:
    """ジャンルマスタ更新を実行します.

    Args:
        force_update: 強制アップデートフラグ
        genre_repository: ジャンルリポジトリ
        tmdb_client: TMDBクライアント
    """

    # 登録済のジャンルIDを全て取得
    genre_id_set = {genre.genre_id for genre in genre_repository.fetch_all()}

    # 英語表記のジャンルを取得
    english_genres = tmdb_client.fetch_genres(MovieLanguage.EN)

    # 日本語表記のジャンルを取得
    japanese_genres = tmdb_client.fetch_genres(MovieLanguage.JP)

    # ジャンルモデルに詰め替える
    genre_list = map_genre_list(
        genre_id_set,
        english_genres.genres,
        japanese_genres.genres,
        force_update
    )

    # モデルの永続化
    count = genre_repository.save(genre_list)

    log.info(f"ジャンルマスタ更新バッチ実行完了. 更新数={count}")


@batch_service
def exec_update_popular_movies(
    page: int,
    force_update: bool,
    tmdb_client: AbstractTmdbClient,
    movie_repository: AbstractMovieRepository
) -> None:
    """人気映画更新を実行します.

    Args:
        page: 対象ページ
        force_update: 強制アップデートフラグ
        tmdb_client: TMDBクライアント
        movie_repository: 映画リポジトリ
    """

    # 登録済の映画IDを取得
    registered_movies = set(movie_repository.fetch_all_movie_id())

    # 人気映画のリストを取得
    popular_movies = tmdb_client.fetch_popular_movies(page)

    # 映画IDリストを取得(登録済の映画は含めないが、強制アップデートフラグありの場合取得)
    movie_id_list = [movie.id for movie in popular_movies.results if movie.id not in registered_movies or force_update]

    # 映画詳細リストを取得
    movie_detail_list = tmdb_client.fetch_movie_detail_list(
        movie_id_list=movie_id_list,
        language=MovieLanguage.JP
    )

    # 映画モデルリストに変換
    movie_list = [movie.to_internal_movie() for movie in movie_detail_list]

    # モデルの永続化
    movie_repository.save_movie_list(movie_list)

    log.info(f"人気映画情報取得バッチ実行完了. 更新数={len(movie_list)}")


@batch_service
def exec_update_movie_reviews(
    tmdb_client: AbstractTmdbClient,
    movie_repository: AbstractMovieRepository,
    review_repository: AbstractReviewRepository
) -> None:
    """映画レビュー更新処理を実行します.

    Args:
        tmdb_client: TMDBクライアント
        movie_repository: 映画リポジトリ
        review_repository: レビューリポジトリ
    """

    # 登録済の映画IDを全て取得
    registered_movie_ids = movie_repository.fetch_all_movie_id()

    # 登録済のレビューIDを全て取得
    registered_review_ids = review_repository.fetch_all_review_id()

    # 映画IDごとにレビューデータを取得・登録していく
    count = update_review_data(
        registered_movie_ids=registered_movie_ids,
        registered_review_ids=registered_review_ids,
        tmdb_client=tmdb_client,
        review_repository=review_repository
    )

    log.info(f"レビューデータ収集バッチ実行終了.  登録数={count}")


@batch_service
def exec_update_similar_movies(
    tmdb_client: AbstractTmdbClient,
    movie_repository: AbstractMovieRepository
) -> None:
    """類似映画更新処理を実行します.

    Args:
        tmdb_client (AbstractTmdbClient): TMDBクライアント
        movie_repository (AbstractMovieRepository): 映画リポジトリ
    """

    # 登録済の映画IDを全て取得
    registered_movies_id_set = set(movie_repository.fetch_all_movie_id())

    # 登録済の類似映画IDを全て取得 (key: movie_id, value: set(similar_movie_id))
    registered_similar_movie_map = movie_repository.fetch_all_similar_movie()

    # 映画IDごとに全ての類似映画を取得
    count = update_similar_movies_data(
        registered_movies_id_set=registered_movies_id_set,
        registered_similar_movie_map=registered_similar_movie_map,
        tmdb_client=tmdb_client,
        movie_repository=movie_repository
    )

    log.info(f"類似映画収集バッチ実行終了.  登録数={count}")
