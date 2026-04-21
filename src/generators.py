from typing import Iterable, Iterator


def filter_by_currency(transactions: Iterable[dict], currency_code: str) -> Iterator[dict]:
    """
    Принимает список словарей и возвращает итератор с транзакциями в заданной валюте.
    """
    for transaction in transactions:
        # проверяем вложенную структуру словаря на соответствие коду валюты
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: Iterable[dict]) -> Iterator[str]:
    """
    Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди.
    """
    for transaction in transactions:
        # Используем .get() для безопасного извлечения описания
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне.
    """
    for number in range(start, stop + 1):
        # Превращаем число в строку из 16 символов, дополняя нулями слева
        card_str = f"{number:016}"

        # Форматируем строку, добавляя пробелы каждые 4 символа
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"

        yield formatted_card

