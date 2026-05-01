import json
import os


def get_financial_transactions(path):
    """
    читает json и возвращает список словарей
    возвращает пустой список, если файл не найден, пуст или содержит не список.
    """
    if not os.path.exists(path):
        return []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []

