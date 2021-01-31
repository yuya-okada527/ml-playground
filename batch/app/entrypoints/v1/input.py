import typer

from core.config import InputDbSettings
from infra.repository.input.genre import GenreRepository
from service.input.movie import update_genre_master


app = typer.Typer()


@app.command("genre")
def submit_genre():
    genre_repository = GenreRepository(InputDbSettings())
    try:
        update_genre_master(genre_repository)
    except Exception as e:
        raise e


if __name__ == "__main__":
    app()
