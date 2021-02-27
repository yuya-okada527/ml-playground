"""類似映画データ構築エントリポイントモジュール

類似映画データをKVS上に構築するバッチのエントリポイントを記述するモジュール

Todo:
    * MLパイプラインとの役割分担を検討
"""
import typer
from infra.repository.input.movie_repository import MovieRepository
from infra.repository.similarity.redis_repository import RedisRepository
from service.similarity_service import exec_construct_tmdb_similarity

app = typer.Typer()


@app.command("tmdb-sim")
def construct_tmdb_similarity_batch() -> None:
    """TMDB API類似映画データ構築バッチ

    TMDB APIに基づく類似映画データを構築します.
    """

    # リポジトリを初期化
    redis_repository = RedisRepository()
    movie_repository = MovieRepository()

    # サービス実行
    exec_construct_tmdb_similarity(
        redis_repository=redis_repository,
        movie_repository=movie_repository
    )
