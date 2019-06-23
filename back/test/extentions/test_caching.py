from typing import Dict
import time
from datetime import timedelta
import json

import pytest

from back.extensions.google.caching import build_caching_key_with_kwargs, redis_cache, redis_client

VALUE = 0


@pytest.fixture(scope="function", autouse=True)
def flush_redis():
    redis_client.flushdb()


@pytest.fixture()
def reset_value():
    global VALUE
    VALUE = 0
    yield
    VALUE = 0


def dummy_function():
    pass


class CustomDataStructure:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def serialize(c):
        return json.dumps({"name": c.name})

    @classmethod
    def deserialize(cls, c):
        name = json.loads(c)["name"]
        return cls(name=name)


class DummyKlass:
    @redis_cache()
    def simple_strings(self, a: str) -> str:
        global VALUE
        VALUE = VALUE + 1
        return a

    @redis_cache(expiry=timedelta(seconds=1))
    def simple_strings_with_expiry(self, a: str) -> str:
        global VALUE
        VALUE = VALUE + 1
        return a

    @redis_cache(serialize=lambda a: json.dumps(a), deserialize=lambda a: json.loads(a))
    def test_json_serialization_deserialization(self, a: str) -> Dict:
        global VALUE
        VALUE = VALUE + 1
        return dict(a=a)

    @redis_cache(serialize=CustomDataStructure.serialize, deserialize=CustomDataStructure.deserialize)
    def test_custom_serialization_deserialization(self, a: str) -> Dict:
        global VALUE
        VALUE = VALUE + 1
        return CustomDataStructure(name=a)


dummy = DummyKlass()


def test_key_generation():
    assert build_caching_key_with_kwargs(dummy_function, {"a": 1, "b": 2}) == "dummy_function:a.1-b.2"
    assert build_caching_key_with_kwargs(dummy_function, {"a": [1, 2], "b": 2}) == "dummy_function:a.[1, 2]-b.2"
    assert build_caching_key_with_kwargs(dummy_function, {"a": dict(a=1, b=1), "b": 2}) == "dummy_function:a.{'a': 1, 'b': 1}-b.2" # noqa
    assert build_caching_key_with_kwargs(dummy_function, {"a": int, "b": 2}) == "dummy_function:a.<class 'int'>-b.2"


def test_cache_decorator_with_strings(reset_value):
    assert VALUE == 0
    result = dummy.simple_strings(a="a")
    assert VALUE == 1
    cached_result = dummy.simple_strings(a="a")
    assert VALUE == 1
    assert result == cached_result
    dummy.simple_strings(a="aa")
    assert VALUE == 2


def test_cache_expiry(reset_value):
    assert VALUE == 0
    dummy.simple_strings_with_expiry(a="a")
    assert VALUE == 1
    dummy.simple_strings_with_expiry(a="a")
    assert VALUE == 1
    time.sleep(1.2 * timedelta(seconds=1).total_seconds())
    dummy.simple_strings_with_expiry(a="a")
    assert VALUE == 2


def test_cache_decorator_with_json_serialization(reset_value):
    assert VALUE == 0
    result = dummy.test_json_serialization_deserialization(a="a")
    assert VALUE == 1
    cached_result = dummy.test_json_serialization_deserialization(a="a")
    assert VALUE == 1
    assert result == cached_result
    dummy.test_json_serialization_deserialization(a="aa")
    assert VALUE == 2


def test_cache_decorator_with_custom_serialization(reset_value):
    assert VALUE == 0
    result = dummy.test_custom_serialization_deserialization(a="first_name")
    assert VALUE == 1
    assert isinstance(result, CustomDataStructure)
    cached_result = dummy.test_custom_serialization_deserialization(a="first_name")
    assert VALUE == 1
    assert isinstance(cached_result, CustomDataStructure)
    assert result.name == cached_result.name
    dummy.test_custom_serialization_deserialization(a="other_name")
    assert VALUE == 2
