"""Модуль автоматического тестирования генераторов транзакций и номеров карт."""
import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions_list():
    """Фикстура, предоставляющая тестовый список финансовых транзакций."""
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод организации"},
        {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Перевод со счета на счет"},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод с карты на карту"},
    ]

# тесты для filter_by_currency


def test_filter_by_currency_valid(transactions_list):
    """Проверка фильтрации транзакций по USD."""
    usd_gen = filter_by_currency(transactions_list, "USD")
    assert next(usd_gen)["id"] == 1
    assert next(usd_gen)["id"] == 3
    with pytest.raises(StopIteration):
        next(usd_gen)


def test_filter_by_currency_empty():
    """Проверка работы с пустым списком."""
    gen = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(gen)


def test_filter_by_currency_no_match(transactions_list):
    """Проверка случая, когда валюта не найдена."""
    gen = filter_by_currency(transactions_list, "EUR")
    with pytest.raises(StopIteration):
        next(gen)


# тесты для transaction_descriptions


def test_transaction_descriptions_valid(transactions_list):
    """Проверка получения описаний транзакций."""
    descriptions = transaction_descriptions(transactions_list)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"


def test_transaction_descriptions_empty():
    """Проверка пустого списка описаний."""
    descriptions = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(descriptions)

# тесты для card_number_generator


@pytest.mark.parametrize("start, stop, expected", [
    (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
    (999, 1000, ["0000 0000 0000 0999", "0000 0000 0000 1000"]),
    (5, 5, ["0000 0000 0000 0005"]),
])
def test_card_number_generator_range(start, stop, expected):
    """Параметризованный тест диапазона и формата номеров карт."""
    gen = card_number_generator(start, stop)
    result = list(gen)
    assert result == expected


def test_card_number_generator_logic():
    """Проверка корректного завершения генератора."""
    gen = card_number_generator(1, 3)
    next(gen)
    next(gen)
    next(gen)
    with pytest.raises(StopIteration):
        next(gen)
