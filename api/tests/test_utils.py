from tests.utils import make_url


def test_make_url_queries_is_None():

    # テストデータ
    path = "/test"
    queries = None

    # 検証
    assert make_url(path, queries) == "/test"

def test_make_url_queries_is_empty():

    # テストデータ
    path = "/test"
    queries = []

    # 検証
    assert make_url(path, queries) == "/test"


def test_make_url_single_queries_exists():

    # テストデータ
    path = "/test"
    queries = [
        "key=value"
    ]

    # 検証
    assert make_url(path, queries) == "/test?key=value"



def test_make_url_multiple_queries_exists():

    # テストデータ
    path = "/test"
    queries = [
        "key=value1",
        "key=value2"
    ]

    # 検証
    assert make_url(path, queries) == "/test?key=value1&key=value2"
