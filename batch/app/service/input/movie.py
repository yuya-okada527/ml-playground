from infra.client.tmdb.api import fetch_genres


def update_genre_master():
    
    # 映画ジャンルの日本語表記を取得
    japanese_genres = fetch_genres("ja")

    # ジャンルIDで集計
    genre_id_dict = {genre.id : genre for genre in japanese_genres.genres}

    print(genre_id_dict)