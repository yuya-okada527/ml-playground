from pprint import pprint

import requests
import typer

from core.config import settings
from infra.client.tmdb.constant import MOVIE_GENRE_LIST_PATH, POPULAR_MOVIE_PATH
from infra.client.tmdb.query import PopularMovieQuery

app = typer.Typer()


@app.command()
def main():
    url = settings.tmdb_url + "/movie/531499/watch/providers"
    query = PopularMovieQuery(
        api_key=settings.tmdb_api_key
    )
    res = requests.get(url=url, params=query.dict())
    pprint(res.json()["results"])



if __name__ == "__main__":
    app()
