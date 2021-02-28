"""入稿エントリポイントモジュール

入稿DB(input_db)にデータを構築する際に使用するバッチのエントリポイントを記述するモジュール
"""
import typer
from core.config import TmdbSettings
from infra.client.tmdb.tmdb_api import TmdbClient
from infra.repository.input.genre_repository import GenreRepository
from infra.repository.input.movie_repository import MovieRepository
from infra.repository.input.review_repository import ReviewRepository
from service.input_service import (exec_update_genre_master,
                                   exec_update_movie_reviews,
                                   exec_update_popular_movies,
                                   exec_update_similar_movies)

app = typer.Typer()


@app.command("genre")
def update_genre_master_batch(force_update: bool = False) -> None:
    """ジャンルマスタ更新バッチ

    ジャンルマスタを最新の状態に更新します.

    Args:
        force_update: 強制アップデートフラグ(Trueの場合、登録済のレコードも更新します)
    """

    # リポジトリの初期化
    genre_repository = GenreRepository()
    # クライアントの初期化
    tmdb_client = TmdbClient(TmdbSettings())

    # サービスの実行
    exec_update_genre_master(
        force_update=force_update,
        genre_repository=genre_repository,
        tmdb_client=tmdb_client
    )


@app.command("movies")
def update_popular_movies_batch(page: int = 1, force_update: bool = False) -> None:
    """人気映画更新バッチ

    TMDBの人気映画APIを元に映画テーブルを更新します.

    Args:
        page: 人気映画取得ページ
        force_update: 強制アップデートフラグ(Trueの場合、登録済のレコードも更新します)
    """

    # クライアントの初期化
    tmdb_client = TmdbClient(TmdbSettings())

    # リポジトリの初期化
    movie_repository = MovieRepository()

    # サービスの実行
    exec_update_popular_movies(
        force_update=force_update,
        page=page,
        tmdb_client=tmdb_client,
        movie_repository=movie_repository
    )


@app.command("reviews")
def update_movie_reviews_batch() -> None:
    """映画レビュー更新バッチ

    映画レビューを更新します.
    """

    # クライアントの初期化
    tmdb_client = TmdbClient(TmdbSettings())

    # リポジトリの初期化
    movie_repository = MovieRepository()
    review_repository = ReviewRepository()

    # サービス実行
    exec_update_movie_reviews(
        tmdb_client=tmdb_client,
        movie_repository=movie_repository,
        review_repository=review_repository
    )


@app.command("similar_movies")
def update_similar_movies_batch() -> None:
    """類似映画更新バッチ

    類似映画を更新します.
    """

    # クライアントの初期化
    tmdb_client = TmdbClient(TmdbSettings())

    # リポジトリの初期化
    movie_repository = MovieRepository()

    # サービス実行
    exec_update_similar_movies(
        tmdb_client=tmdb_client,
        movie_repository=movie_repository
    )


if __name__ == "__main__":
    app()
