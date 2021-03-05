from domain.enums.movie_enums import MovieField
from infra.client.solr.solr_query import SolrFilterQuery
from service.logic.movie_logic import _build_free_word_query


def test_build_free_word_query():

    # テストデータ
    q = ["test1", "test2"]

    # 検証
    actual = _build_free_word_query(q)
    expected = [
        SolrFilterQuery.exact_condition(field=MovieField.FREE_WORD, value="test1"),
        SolrFilterQuery.exact_condition(field=MovieField.FREE_WORD, value="test2")
    ]

    assert actual == expected
