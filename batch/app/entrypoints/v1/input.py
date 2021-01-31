import typer

from core.config import InputDbSettings, TmdbSettings
from infra.client.tmdb.api import TmdbClient
from infra.repository.input.genre import GenreRepository
from service.input.movie import update_genre_master


app = typer.Typer()


@app.command("genre")
def submit_genre():
    genre_repository = GenreRepository(InputDbSettings())
    tmdb_client = TmdbClient(TmdbSettings())
    try:
        update_genre_master(genre_repository, tmdb_client)
    except Exception as e:
        raise e





if __name__ == "__main__":
    app()
