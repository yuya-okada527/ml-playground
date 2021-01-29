from pprint import pprint

import requests
import typer

from app.core.config import settings
from app.infra.client.tmdb.query import PopularMovieQuery

app = typer.Typer()


@app.command()
def main():
    url = settings.tmdb_url + "/movie/popular"
    query = PopularMovieQuery(
        api_key=settings.tmdb_api_key
    )
    res = requests.get(url=url, params=query.dict())
    pprint(len(res.json()["results"]))



if __name__ == "__main__":
    app()
