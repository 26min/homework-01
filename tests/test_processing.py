import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    return [
        {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    ]


def test_filter_by_state_default(sample_data):
    """Тест фильтрации по умолчанию (EXECUTED)."""
    result = filter_by_state(sample_data)
    assert len(result) == 2
    assert result[0]['id'] == 414288290
    assert result[1]['id'] == 939719570


def test_filter_by_state_canceled(sample_data):
    """Тест фильтрации по статусу (CANCELED)."""
    result = filter_by_state(sample_data, state="CANCELED")
    assert len(result) == 1
    assert result[0]['id'] == 594226727


def test_sort_by_date_descending(sample_data):
    """Тест сортировки по убыванию (от свежих к старым)."""
    result = sort_by_date(sample_data, descending=True)
    assert result[0]['id'] == 414288290  # 2019 год
    assert result[1]['id'] == 594226727  # сентябрь 2018
    assert result[2]['id'] == 939719570  # июнь 2018


def test_sort_by_date_ascending(sample_data):
    """Тест сортировки по возрастанию (от старых к свежим)."""
    result = sort_by_date(sample_data, descending=False)
    assert result[0]['id'] == 939719570  # июнь 2018
    assert result[1]['id'] == 594226727  # сентябрь 2018
    assert result[2]['id'] == 414288290  # 2019 год
