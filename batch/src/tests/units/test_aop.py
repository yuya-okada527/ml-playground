from enum import Enum

from app.core.aop import _filter_params, _is_batch_args


def test_filter_params_basic_type_remains():

    # テストデータ
    kwargs = {
        "str": "test",
        "int": 3,
        "float": 2.1,
        "bool": True,
        "enum": SampleEnum.TEST,
        "list": ["test"],
        "set": {"test"},
        "dict": {"key": "value"}
    }

    assert _filter_params(kwargs) == kwargs


def test_filter_params_not_basic_type_removed():

    # テストデータ
    kwargs = {
        "repository": SampleClass()
    }

    assert _filter_params(kwargs) == {}


def test_is_batch_args_basic_type():

    assert _is_batch_args("test")
    assert _is_batch_args(3)
    assert _is_batch_args(2.3)
    assert _is_batch_args(True)
    assert _is_batch_args(SampleEnum.TEST)
    assert _is_batch_args(["test"])
    assert _is_batch_args({"test"})
    assert _is_batch_args({"key": "value"})


def test_is_batch_args_not_basic_type():

    assert _is_batch_args(SampleClass()) == False


class SampleEnum(Enum):
    TEST = "test"


class SampleClass():
    ...
