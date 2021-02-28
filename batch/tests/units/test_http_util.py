
import pytest
from domain.exceptions.http_exception import ClientSideError, ServerSideError
from pydantic.main import BaseModel
from requests.models import Response
from util.http_util import _check_status_code, _data_to_string, retry_exec


def test_data_to_string_str():

    # テストデータ
    data = "str"

    # 検証
    assert _data_to_string(data) == "str"


def test_data_to_string_dict():

    # テストデータ
    data = {
        "key": "value"
    }

    # 検証
    assert _data_to_string(data) == '{"key": "value"}'


def test_data_to_string_base_model():

    # テストデータ
    data = SampleModel(key="value")

    # 検証
    assert _data_to_string(data) == '{"key": "value"}'


def test_check_status_code_400():

    # テストデータ
    response = FakeResponse(status_code=400)

    # 検証
    with pytest.raises(ClientSideError):
        _check_status_code(response)


def test_check_status_code_499():

    # テストデータ
    response = FakeResponse(status_code=499)

    # 検証
    with pytest.raises(ClientSideError):
        _check_status_code(response)


def test_check_status_code_500():

    # テストデータ
    response = FakeResponse(status_code=500)

    # 検証
    with pytest.raises(ServerSideError):
        _check_status_code(response)


def test_check_status_code_399():

    # テストデータ
    response = FakeResponse(status_code=399)

    # 検証
    assert _check_status_code(response) is None


def test_retry_exec_retry_max_times():

    # テストデータ
    count = []
    max_retry_num = 2
    wait_time_base = 1
    @retry_exec(max_retry_num=max_retry_num, wait_time_base=wait_time_base)
    def fake_http_request(count):
        count.append(True)
        raise ServerSideError()

    # 検証
    try:
        fake_http_request(count)
    except ServerSideError:
        pass

    assert sum(count) == max_retry_num



class SampleModel(BaseModel):
    key: str


class FakeResponse(Response):

    def __init__(self, status_code) -> None:
        self.status_code = status_code

    def json(self):
        return {}
