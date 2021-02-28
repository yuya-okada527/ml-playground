"""出稿ロジックモジュール

出稿バッチに関するロジック関数を提供するモジュール
"""
from typing import Any

from core.constants import HALF_SPACE
from domain.models.internal.movie_model import Movie
from domain.models.solr.solr_movie_model import MovieSolrModel
from domain.models.solr.solr_schema_model import SolrSchemaModel


def calculate_difference(
    current_schema: SolrSchemaModel,
    update_schema: dict[str, Any]
) -> dict[str, Any]:
    """差分スキーマ計算関数

    現在のschemaと更新対象のスキーマの差分を計算する
    """

    # 現在のスキーマのフィールドタイプ名をセットに変換
    current_field_type_set = {field_type["name"] for field_type in current_schema.fieldTypes}

    # フィールドタイプの差分を検知
    add_field_type = []
    replace_field_type = []
    for field_type in update_schema.get("fieldTypes", []):
        # 同名のフィールドタイプがある場合、replace
        if field_type["name"] in current_field_type_set:
            replace_field_type.append(field_type)
        # 新規のフィールドタイプの場合、add
        else:
            add_field_type.append(field_type)

    # 現在のスキーマのフィールド名をセットに変換
    current_field_set = {field["name"] for field in current_schema.fields_}

    # フィールドの差分を検知
    add_field = []
    replace_field = []
    for field in update_schema.get("fields", []):
        # 同名のフィールドタイプがある場合、replace
        if field["name"] in current_field_set:
            replace_field.append(field)
        # 新規のフィールドタイプの場合、add
        else:
            add_field.append(field)

    # TODO スキーマクラスを実装
    return {
        "add-field-type": add_field_type,
        "replace-field-type": replace_field_type,
        "add-field": add_field,
        "replace-field": replace_field
    }


def map_to_solr_model(movie: Movie, exec_time: int) -> MovieSolrModel:
    """Solrモデルに対するマッピングを実施する.

    Args:
        movie (Movie): 映画モデル
        exec_time (int): 実行日時

    Returns:
        MovieSolrModel: Solr映画モデル
    """
    return MovieSolrModel(
        movie_id=movie.movie_id,
        free_word=_make_freeword(movie),
        original_title=movie.original_title,
        japanese_title=movie.japanese_title,
        overview=movie.overview,
        tagline=movie.tagline,
        poster_path=movie.poster_path,
        backdrop_path=movie.backdrop_path,
        popularity=movie.popularity,
        vote_average=movie.vote_average,
        release_date=movie.release_date_str,
        release_year=movie.release_year,
        genres=[genre.genre_id for genre in movie.genres],
        genre_labels=[genre.japanese_name for genre in movie.genres],
        index_time=exec_time
    )


def _make_freeword(movie: Movie) -> str:
    """フリーワードを作成する.

    Args:
        movie (Movie): 映画モデル

    Returns:
        str: フリーワード
    """

    # フリーワードの要素を保持
    free_word_list = []

    # タイトル
    free_word_list.append(movie.original_title)
    free_word_list.append(movie.japanese_title)

    # ジャンル
    free_word_list.extend([genre.japanese_name for genre in movie.genres])

    # 半角スペース区切りで返す
    return HALF_SPACE.join([free_word for free_word in free_word_list if free_word])
