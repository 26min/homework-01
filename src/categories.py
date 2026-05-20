"""Модуль поиска и подсчета категорий."""
import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Ищет банковские операции по ключевому слову в описании."""
    if not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    matching_transactions = []

    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            matching_transactions.append(transaction)

    return matching_transactions


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций для заданных категорий.

    Категории ищутся в поле 'description'. Категории, отсутствующие
    в списке или в данных, инициализируются нулевым значением.
    """
    result = {category: 0 for category in categories}
    if not data:
        return result

    # Собираем все описания из транзакций
    descriptions = [
        transaction.get("description")
        for transaction in data
        if transaction.get("description")
    ]

    # Считаем вхождения с помощью Counter
    counts = Counter(descriptions)

    for category in categories:
        result[category] = counts.get(category, 0)

    return result
