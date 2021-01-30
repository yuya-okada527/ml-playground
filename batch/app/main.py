import typer

from entrypoints.v1 import submit

app = typer.Typer()
app.add_typer(submit.app, name="submit")


if __name__ == "__main__":
    app()
