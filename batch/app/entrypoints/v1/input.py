import typer

from service.input.movie import update_genre_master


app = typer.Typer()


@app.command("genre")
def submit_genre():
    try:
        update_genre_master()
    except Exception as e:
        typer.echo(e)


if __name__ == "__main__":
    app()
