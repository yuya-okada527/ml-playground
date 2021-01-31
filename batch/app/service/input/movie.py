from domain.models.internal.movie import Genre
from infra.client.tmdb.api import AbstractTmdbClient
from infra.repository.input.genre import AbstractGenreRepository


def update_genre_master(genre_repository: AbstractGenreRepository, tmdb_client: AbstractTmdbClient):
    
    # 英語表記のジャンルを取得
    english_genres = tmdb_client.fetch_genres("en-US")

    # ジャンルIDで集計
    genre_id_dict = {genre.id : genre for genre in english_genres.genres}

    # 日本語表記のジャンルを取得
    japanese_genres = tmdb_client.fetch_genres("ja")

    # RDBモデルに詰め替える
    genre_list = []
    for jp_genre in japanese_genres.genres:
        en_genre = genre_id_dict.get(jp_genre.id)

        # 日本語表記と英語表記が一致しない場合はスキップ
        if not en_genre:
            print(jp_genre)
            continue

        genre_list.append(Genre(
            genre_id=en_genre.id, 
            name=en_genre.name, 
            japanese_name=jp_genre.name)
        )

    # モデルの永続化
    genre_repository.save(genre_list)
