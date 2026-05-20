"""Модуль тестирования функций поиска и подсчета категорий транзакций."""

from src.categories import process_bank_operations, process_bank_search


def test_process_bank_search_success() -> None:
    """Тест успешного поиска транзакций по ключевому слову в описании."""
    data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод со счета на счет"},
    ]
    result = process_bank_search(data, "перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_process_bank_search_empty_or_no_match() -> None:
    """Тест поиска при пустом запросе или отсутствии совпадений."""
    data = [{"id": 1, "description": "Открытие вклада"}]
    assert process_bank_search(data, "") == []
    assert process_bank_search(data, "Кредит") == []


def test_process_bank_operations_success() -> None:
    """Тест корректного подсчета категорий с использованием Counter."""
    data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод организации"},
    ]
    categories = ["Перевод организации", "Открытие вклада", "Покупка"]

    result = process_bank_operations(data, categories)
    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1
    assert result["Покупка"] == 0


def test_process_bank_operations_empty() -> None:
    """Тест подсчета категорий при пустом списке транзакций."""
    categories = ["Перевод организации"]
    result = process_bank_operations([], categories)
    assert result["Перевод организации"] == 0
