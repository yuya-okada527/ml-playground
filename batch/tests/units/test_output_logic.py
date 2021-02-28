from domain.models.internal.movie_model import Genre, Movie
from domain.models.solr.solr_schema_model import SolrSchemaModel
from service.logic.output_logic import _make_freeword, calculate_difference


def test_make_freeword():

    # テストデータ
    movie = Movie(
        movie_id=0,
        original_title="original_title",
        japanese_title="japanese_title",
        genres=[
            Genre(
                genre_id=0,
                name="name0",
                japanese_name="名前0"
            ),
            Genre(
                genre_id=1,
                name="name1",
                japanese_name="名前1"
            )
        ]
    )

    # 検証
    actual = _make_freeword(movie)
    expected = "original_title japanese_title 名前0 名前1"

    assert actual == expected


def test_make_freeword_when_empty_element_exists():

    # テストデータ
    movie = Movie(
        movie_id=0,
        original_title="",
        japanese_title=None,
        genres=[]
    )

    # 検証
    actual = _make_freeword(movie)
    expected = ""

    assert actual == expected


def test_calculate_difference():

    # テストデータ
    current_schema = SolrSchemaModel(
        name="name",
        version=0.1,
        uniqueKey="uniqueKey",
        fieldTypes=[
            {
                "name": "type_name1"
            }
        ],
        fields=[
            {
                "name": "name1",
                "type": "type_name1"
            }
        ]
    )
    update_schema = {
        "fieldTypes": [
            {
                "name": "type_name1"
            },
            {
                "name": "type_name2",
                "hoge": "fuga"
            }
        ],
        "fields": [
            {
                "name": "name1",
                "type": "type_name2"
            },
            {
                "name": "name2",
                "type": "type_name1"
            }
        ]
    }

    # 検証
    actual = calculate_difference(
        current_schema=current_schema,
        update_schema=update_schema
    )
    expected = {
        "add-field-type": [{
            "name": "type_name2",
            "hoge": "fuga"
        }],
        "replace-field-type": [{
            "name": "type_name1"
        }],
        "add-field": [{
            "name": "name2",
            "type": "type_name1"
        }],
        "replace-field": [{
            "name": "name1",
            "type": "type_name2"
        }]
    }

    assert actual == expected
