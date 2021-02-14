import typer

from infra.repository.input.movie import MovieRepository
from infra.repository.sim.redis_repository import RedisRepository
from service.sim.sim_movie_service import exec_construct_tmdb_similarity


app = typer.Typer()


@app.command("tmdb-sim")
def construct_tmdb_similarity():

    # リポジトリを初期化
    redis_repository = RedisRepository()
    movie_repository = MovieRepository()

    # サービス実行
    exec_construct_tmdb_similarity(
        redis_repository=redis_repository,
        movie_repository=movie_repository
    )
