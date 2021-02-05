import typer

from core.config import InputDbSettings, TmdbSettings
from infra.client.tmdb.api import TmdbClient
from infra.repository.input.genre import GenreRepository
from infra.repository.input.movie import MovieRepository
from service.input.movie import update_genre_master, update_movies


app = typer.Typer()


@app.command("genre")
def input_genre():

    # リポジトリの初期化
    genre_repository = GenreRepository()
    # クライアントの初期化
    tmdb_client = TmdbClient(TmdbSettings())

    # サービスの実行
    update_genre_master(genre_repository=genre_repository, tmdb_client=tmdb_client)


@app.command("movies")
def input_movies(page: int = 1):

    # クライアントの初期化
    tmdb_client = TmdbClient(TmdbSettings())

    # リポジトリの初期化
    movie_repository = MovieRepository()

    # サービスの実行
    update_movies(page=page, tmdb_client=tmdb_client, movie_repository=movie_repository)


if __name__ == "__main__":
    app()
