import typer


def main(name: str):
    typer.echo("Hello World")


if __name__ == "__main__":
    typer.run(main)
