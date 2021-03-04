from domain.models.solr.movies import (MovieSolrModel, SolrResponseModel,
                                       SolrResultModel)
from fastapi.testclient import TestClient
from infra.client.solr.solr_api import get_solr_client
from infra.client.solr.solr_query import SolrQuery
from main import app
from tests.utils import make_url

# サーチAPIパス
V1_SEARCH_API_PATH = "/v1/movie/search"
# 映画ID APIパス
V1_SEARCH_BY_ID_API_PATH = "/v1/movie/search/{movie_id}"

client = TestClient(app)


async def get_fake_solr_client():
    return FakeSolrClient()


app.dependency_overrides[get_solr_client] = get_fake_solr_client


def test_search_api_200():

    # 正常ケースパラメータリスト
    # TODO pytestのパラメータテスト使う？
    param_list = [
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
    ]
    for params in param_list:
        url = make_url(V1_SEARCH_API_PATH, params)
        response = client.get(url)
        assert response.status_code == 200, f"params={params} test failed."


def test_search_by_id_api_200():
    url = V1_SEARCH_BY_ID_API_PATH.format(movie_id=0)
    response = client.get(url)
    assert response.status_code == 200


def test_search_api_422():

    # バリデーションエラーケースリスト
    param_list = [
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
    ]
    for params in param_list:
        url = make_url(V1_SEARCH_API_PATH, params)
        response = client.get(url)
        assert response.status_code == 422, f"params={params} test failed."

# TODO 映画ID APIの空振りシナリオ

class FakeSolrClient:

    def search_movies(self, query: SolrQuery) -> SolrResultModel:
        return SolrResultModel(
            responseHeader=None,
            response=SolrResponseModel(
                numFound=1,
                start=0,
                numFoundExact=True,
                docs=[
                    MovieSolrModel(
                        movie_id=0,
                        original_title="original_title",
                        japanese_title="japanese_title",
                        poster_path="poster_path",
                        popularity=0,
                        vote_average=0
                    )
                ]
            )
        )
