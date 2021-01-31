import typer

from core.config import InputDbSettings, TmdbSettings
from infra.client.tmdb.api import TmdbClient
from infra.repository.input.genre import GenreRepository
from service.input.movie import update_genre_master, update_movies


app = typer.Typer()


@app.command("genre")
def submit_genre():

    # リポジトリの初期化
    genre_repository = GenreRepository(InputDbSettings())
    # クライアントの初期化
    tmdb_client = TmdbClient(TmdbSettings())

    # サービスの実行
    update_genre_master(genre_repository=genre_repository, tmdb_client=tmdb_client)


@app.command("movies")
def submit_movies(page: int = 1):

    # クライアントの初期化
    tmdb_client = TmdbClient(TmdbSettings())

    # サービスの実行
    update_movies(page=page, tmdb_client=tmdb_client)




if __name__ == "__main__":
    app()
