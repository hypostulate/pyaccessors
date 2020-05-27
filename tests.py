import pytest
from pyaccessors import *

# python -m pytest --cov-report term-missing -s --cov=pyaccessors tests.py


@pytest.fixture
def schema_list():
    fields = [
        "a",
        "b",
        "c",
    ]

    values = [
        "A",
        "B",
        "C",
    ]

    data_list = []
    for i in range(0, 3):
        data_list.append({f: f"{v}{i}" for f, v in zip(fields, values)})
    return data_list


@pytest.fixture
def schema_dict(schema_list):
    return schema_list[0]


def test_field_access_unique_vals(schema_list):
    key = "a"
    access_dict = access(schema_list, key)
    expected = {obj[key]: obj for obj in schema_list}
    assert access_dict == expected


def test_single_dict_access(schema_dict):
    key = "a"
    access_dict = access(schema_dict, key)
    expected = {obj[key]: obj for obj in [schema_dict]}
    assert access_dict == expected


def test_field_access_multi_vals_group():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A1", "b": 2},
        {"a": "A2", "b": 3},
    ]

    access_dict = access(case, "a", group=True)
    expected = {
        "A1": [{"a": "A1", "b": 1}, {"a": "A1", "b": 2},],
        "A2": [{"a": "A2", "b": 3},],
    }

    assert access_dict == expected


def test_field_access_multi_vals_no_group():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A1", "b": 2},
        {"a": "A2", "b": 3},
    ]

    with pytest.raises(ValueError):
        access_dict = access(case, "a", group=False)


def test_access_strict_groups_pass():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A1", "b": 2},
        {"a": "A2", "b": 3},
    ]

    access_dict = access(case, "a", group=True)
    expected = {
        "A1": [{"a": "A1", "b": 1}, {"a": "A1", "b": 2},],
        "A2": [{"a": "A2", "b": 3},],
    }

    assert access_dict == expected


def test_access_strict_groups_fail():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A1", "b": 2},
        {"b": 3},
    ]

    with pytest.raises(KeyError):
        access_dict = access(case, "a", group=True, strict=True)


def test_access_strict_wrong_type():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A1", "b": 2},
        {"b": 3},
    ]

    with pytest.raises(TypeError):
        access_dict = access(case, "a", "b")


def test_access_by_wrong_type():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A1", "b": 2},
        {"b": 3},
    ]

    with pytest.raises(TypeError):
        access_dict = access(case, {"A":1})


def test_access_strict_failure():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A2", "b": 2},
        {"b": 3},
    ]
    with pytest.raises(KeyError):
        access_dict = access(case, "a", strict=True)


def test_access_bad_input():
    case = 1
    with pytest.raises(ValueError):
        access(case, "a")


def test_access_nested():
    case = [
        {"a": "A1", "b": {"c": 1}},
        {"a": "A1", "b": {"c": 2}},
        {"a": "A2", "b": {"c": 3}},
    ]

    expected = {
        1: {"a": "A1", "b": {"c": 1}},
        2: {"a": "A1", "b": {"c": 2}},
        3: {"a": "A2", "b": {"c": 3}},
    }

    access_dict = access(case, by=["b", "c"])

    assert access_dict == expected


def test_access_nested_fail():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A1", "b": {"c": 2}},
        {"a": "A2", "b": {"c": 3}},
    ]

    with pytest.raises(KeyError):
        access_dict = access(case, by=["b", "c"], strict=True)


def test_access_nested_messy():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A1", "b": {"c": 2}},
        {"a": "A2", "b": {"c": 3}},
    ]

    expected = {
        2: {"a": "A1", "b": {"c": 2}},
        3: {"a": "A2", "b": {"c": 3}},
    }

    access_dict = access(case, by=["b", "c"])
    assert access_dict == expected


def test_access_nested_messy_group():
    case = [
        {"a": "A1", "b": 1},
        {"a": "A1", "b": {"c": 2}},
        {"a": "A2", "b": {"c": 3}},
        {"a": "A3", "b": {"c": 3, "d": "5"}},
    ]

    expected = {
        2: [{"a": "A1", "b": {"c": 2}}],
        3: [{"a": "A2", "b": {"c": 3}}, {"a": "A3", "b": {"c": 3, "d": "5"}},],
    }

    access_dict = access(case, by=["b", "c"], group=True)
    assert access_dict == expected
