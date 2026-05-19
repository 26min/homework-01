import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
        {"id": 2, "state": "CANCELED", "date": "2018-06-16T12:04:07.309407"},
        {"id": 3, "state": "EXECUTED", "date": "2019-07-26T10:50:58.294041"},
    ]


def test_filter_by_state(sample_data):
    result = filter_by_state(sample_data, "EXECUTED")
    assert len(result) == 2


def test_sort_by_date_default(sample_data):
    result = sort_by_date(sample_data)
    assert result[0]["id"] == 1
