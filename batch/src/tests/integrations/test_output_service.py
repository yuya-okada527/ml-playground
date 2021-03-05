from service.output_service import exec_build_index, exec_update_solr_schema
from tests.utils import FakeMoviewRepository, FakeSolrClient


def test_exec_update_solr_schema():

    # 例外が出ないことを検証
    exec_update_solr_schema(
        solr_client=FakeSolrClient()
    )


def test_exec_build_index():

    # 例外が出ないことを検証
    exec_build_index(
        solr_client=FakeSolrClient(),
        movie_repository=FakeMoviewRepository()
    )
