import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными для фильтрации и сортировки."""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 2, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 3, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    ]


# --- Тесты для filter_by_state ---

def test_filter_by_state_default(sample_data):
    """Тест фильтрации по умолчанию (EXECUTED)."""
    result = filter_by_state(sample_data)
    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[1]['id'] == 2


def test_filter_by_state_canceled(sample_data):
    """Тест фильтрации по явно указанному статусу CANCELED."""
    result = filter_by_state(sample_data, state='CANCELED')
    assert len(result) == 1
    assert result[0]['id'] == 3


def test_filter_by_state_empty_result(sample_data):
    """Тест фильтрации, если совпадений по статусу нет."""
    assert filter_by_state(sample_data, state='PENDING') == []


# --- Тесты для sort_by_date ---

def test_sort_by_date_descending(sample_data):
    """Тест сортировки по дате по убыванию (сначала свежие)."""
    result = sort_by_date(sample_data, descending=True)
    assert result[0]['id'] == 1  # 2019 год
    assert result[1]['id'] == 3  # Сентябрь 2018 года
    assert result[2]['id'] == 2  # Июнь 2018 года


def test_sort_by_date_ascending(sample_data):
    """Тест сортировки по дате по возрастанию (сначала старые)."""
    result = sort_by_date(sample_data, descending=False)
    assert result[0]['id'] == 2  # Июнь 2018 года
    assert result[1]['id'] == 3  # Сентябрь 2018 года
    assert result[2]['id'] == 1  # 2019 год

