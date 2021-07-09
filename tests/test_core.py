import pytest

from eyeson_flask import core


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


def test_get_jumps(get_id):
    assert core.get_jumps(get_id) >= 0


def test_num_stargates(get_id):
    assert core.num_stargates(get_id) == 4


def test_get_recent_kills(get_id):
    assert len(core.get_recent_kills(get_id)) > 0


def test_get_kills_dict(get_id):
    test_dict = core.get_kills_dict(get_id, 1)
    assert len(test_dict) > 0


def test_create_objects():
    object_list = core.create_objects(2)
    assert object_list[1].name == ""


def test_fill_in_object():
    victim = core.Victim
    kill_id = "93457634"
    kill_hash = "b3dd6172ed69518da0484796b18bb5b5c0695c88"
    core.fill_in_object(victim, kill_id, kill_hash)
    assert victim.name != 0
