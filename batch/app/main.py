import typer

from entrypoints.v1 import input

app = typer.Typer()
app.add_typer(input.app, name="input")


if __name__ == "__main__":
    app()
