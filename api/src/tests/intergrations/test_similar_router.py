import pytest
from fastapi.testclient import TestClient
from infra.client.solr.solr_api import get_solr_client
from infra.repository.kvs_repository import get_kvs_repository
from main import app
from tests.utils import get_fake_kvs_repository, get_fake_solr_client, make_url

# 類似映画APIパス
SIMILAR_MOVIE_API_PATH = "/v1/movie/similar/{movie_id}"


client = TestClient(app)

# DIのFake化
app.dependency_overrides[get_solr_client] = get_fake_solr_client
app.dependency_overrides[get_kvs_repository] = get_fake_kvs_repository


@pytest.mark.parametrize("params", [
        # TMDB
        ["model_type=tmdb-sim"],
        # Glove
        ["model_type=glove-sim"]
    ])
def test_similar_movie_api_200(params):

    url = make_url(SIMILAR_MOVIE_API_PATH.format(movie_id=0), params)
    response = client.get(url)
    assert response.status_code == 200, f"params={params} test failed. url={url}"
