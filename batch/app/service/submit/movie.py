from infra.client.tmdb.api import fetch_genres


def update_genre_master():
    res = fetch_genres("ja")
    print(res)