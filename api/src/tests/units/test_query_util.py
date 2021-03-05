from util.query_util import split_query_params


def test_split_query_params_when_value_is_none():

    # テストデータ
    value = None

    # 検証
    assert split_query_params(value) == []


def test_split_query_params_when_value_is_empty():

    # テストデータ
    value = ""

    # 検証
    assert split_query_params(value) == []


def test_split_query_params_split():

    # テストデータ
    value = "v1 v2　v3,v4"

    # 検証
    assert split_query_params(value) == ["v1", "v2", "v3", "v4"]


def test_split_query_params_single_value():

    # テストデータ
    value = "value"

    # 検証
    assert split_query_params(value) == ["value"]


def test_split_query_params_type_func_is_int():

    # テストデータ
    value = "1"

    # 検証
    assert split_query_params(value, int) == [1]
