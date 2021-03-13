from infra.client.solr.solr_query import SolrQuery
from service.logic.movie_logic import (_build_free_word_query,
                                       build_search_query)


def test_build_free_word_query_multi_keyword():

    # テストデータ
    q = ["test1", "test2"]

    # 検証
    actual = _build_free_word_query(q)
    expected = "free_word:test1 AND free_word:test2"

    assert actual == expected


def test_build_free_word_query_single_keyword():

    # テストデータ
    q = ["test"]

    # 検証
    assert _build_free_word_query(q) == "free_word:test"


def test_build_free_word_query_empty():

    # テストデータ
    q = []

    # 検証
    assert _build_free_word_query(q) == "*:*"
