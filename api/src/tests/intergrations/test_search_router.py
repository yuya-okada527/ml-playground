import pytest
from fastapi.testclient import TestClient
from infra.client.solr.solr_api import get_solr_client
from main import app
from tests.utils import get_fake_solr_client, make_url

# サーチAPIパス
V1_SEARCH_API_PATH = "/v1/movie/search"
# サーチ BY ID APIパス
V1_SEARCH_BY_ID_API_PATH = "/v1/movie/search/{movie_id}"
# 映画ID APIパス
V1_SEARCH_MOVIE_ID_API_PATH = "/v1/movie/search/id/all"

client = TestClient(app)

# DIのFake化
app.dependency_overrides[get_solr_client] = get_fake_solr_client


@pytest.mark.parametrize("params", [
        # queryなし
        [],
        # queryあり
        ["query=test"],
        # query空
        ["query="],
        # query100文字,
        ["query=" + "a" * 100],
        # start数字
        ["start=1"],
        # start Min
        ["start=0"],
        # start Max
        ["start=1000"],
        # rows数字
        ["rows=10"],
        # rows Min
        ["rows=1"],
        # rows Max
        ["rows=50"],
        # start & rows
        ["query=test", "start=0", "rows=10"]
    ])
def test_search_api_200(params):
    url = make_url(V1_SEARCH_API_PATH, params)
    response = client.get(url)
    assert response.status_code == 200, f"params={params} test failed. url={url}"


def test_search_by_id_api_200():
    url = V1_SEARCH_BY_ID_API_PATH.format(movie_id=0)
    response = client.get(url)
    assert response.status_code == 200


def test_search_movie_ids():
    url = V1_SEARCH_MOVIE_ID_API_PATH
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("params", [
        # query max_length違反
        ["query=" + "a" * 101],
        # start < 0
        ["start=-1"],
        # start > 1000
        ["start=1001"],
        # rows < 1
        ["rows=0"],
        # rows > 50
        ["rows=51"]
    ])
def test_search_api_422(params):
    url = make_url(V1_SEARCH_API_PATH, params)
    response = client.get(url)
    assert response.status_code == 422, f"params={params} test failed. url={url}"

# TODO 映画ID APIの空振りシナリオ
