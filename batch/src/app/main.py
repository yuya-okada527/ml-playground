import typer

app = typer.Typer()


@app.command()
def main(name: str, flg: bool = False):
    typer.echo("main")


@app.command()
def sub():
    typer.echo("sub")


if __name__ == "__main__":
    app()
