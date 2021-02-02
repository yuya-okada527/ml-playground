import typer

from entrypoints.v1 import input, output

app = typer.Typer()
app.add_typer(input.app, name="input")
app.add_typer(output.app, name="output")


if __name__ == "__main__":
    app()
