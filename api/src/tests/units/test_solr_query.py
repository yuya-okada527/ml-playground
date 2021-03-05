from domain.enums.movie_enums import MovieField
from infra.client.solr.solr_query import (SolrFilterQuery, SolrQuery,
                                          SolrSortQuery, SortDirection)


def test_solr_filter_query_exact_condition():

    # テストデータ
    field = MovieField.FREE_WORD
    value = "hoge"

    # 検証
    actual = SolrFilterQuery.exact_condition(
        field=field,
        value=value
    )
    expected = SolrFilterQuery(
        field=MovieField.FREE_WORD,
        condition="hoge"
    )

    assert actual == expected


def test_solr_filter_query_exact_condition_empty_value():

    # テストデータ
    field = MovieField.FREE_WORD
    value = ""

    # 検証
    actual = SolrFilterQuery.exact_condition(
        field=field,
        value=value
    )

    assert actual is None


def test_solr_filter_query_exact_condition_none_value():

    # テストデータ
    field = MovieField.FREE_WORD
    value = None

    # 検証
    actual = SolrFilterQuery.exact_condition(
        field=field,
        value=value
    )

    assert actual is None


def test_solr_filter_query_get_query_string():

    # テストデータ
    query = SolrFilterQuery.exact_condition(
        field=MovieField.FREE_WORD,
        value="test"
    )

    # 検証
    assert query.get_query_string() == "free_word:test"


def test_solr_filter_query_get_query_string_if_condition_is_empty():

    # テストデータ
    query = SolrFilterQuery(
        field=MovieField.FREE_WORD,
        condition=""
    )

    # 検証
    assert query.get_query_string() is None


def test_solr_filter_query_is_true_if_field_and_condition_exists():

    # テストデータ
    query = SolrFilterQuery(
        field=MovieField.FREE_WORD,
        condition="hoge"
    )

    # 検証
    assert query


def test_solr_filter_query_is_false_if_field_nor_condition_does_not_exist():

    # テストデータ
    query = SolrFilterQuery(
        field=MovieField.FREE_WORD,
        condition=""
    )

    # 検証
    assert not query


def test_solr_sort_query_get_query_string():

    # テストデータ
    query = SolrSortQuery(
        field=MovieField.POPULARITY,
        direction=SortDirection.ASC
    )

    # 検証
    assert query.get_query_string() == "popularity asc"


def test_solr_query_get_query_string():

    # テストデータ
    query = SolrQuery(
        fq=[
            SolrFilterQuery.exact_condition(field=MovieField.FREE_WORD, value="test1"),
            SolrFilterQuery.exact_condition(field=MovieField.MOVIE_ID, value="test2")
        ],
        fl=[
            MovieField.FREE_WORD,
            MovieField.MOVIE_ID
        ],
        start=0,
        rows=10,
        sort=[
            SolrSortQuery(field=MovieField.POPULARITY, direction=SortDirection.ASC),
            SolrSortQuery(field=MovieField.MOVIE_ID, direction=SortDirection.DESC)
        ]
    )

    # 検証
    actual = query.get_query_string()
    expected = "q=*:*&start=0&rows=10&fq=free_word:test1&fq=movie_id:test2&fl=free_word,movie_id&sort=popularity asc,movie_id desc"

    assert actual == expected
