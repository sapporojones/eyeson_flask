import pytest

from eyeson_flask import translators


@pytest.fixture
def get_id():
    sys_id = 30004759
    return sys_id


@pytest.fixture
def get_name():
    sys_name = "1DQ1-A"
    return sys_name


@pytest.fixture
def get_timestamp():
    timestamp = "2021-06-04T01:25:26Z"
    return timestamp


def test_name2id(get_name, get_id):
    assert translators.name2id(get_name) == get_id


def test_id2name(get_id):
    assert translators.id2name(get_id) == "1DQ1-A"


def test_timestamper(get_timestamp):
    ts = translators.timestamper(get_timestamp)
    assert "ago" in ts
