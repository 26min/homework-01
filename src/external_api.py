"""Модуль с конвертацией валюты."""
import os

import requests
from dotenv import load_dotenv

# загружаем переменные окружения
load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")


def convert_to_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли через Exchange Rates Data API.

    Принимает словарь транзакции, возвращает сумму (float).
    """
    # извлекаем данные из вложенной структуры json
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency_code = operation_amount.get("currency", {}).get("code")

    # если валюта уже в рублях, возвращаем как есть
    if currency_code == "RUB":
        return amount

    # если валюта USD или EUR, делаем запрос к API
    if currency_code in ["USD", "EUR"]:
        url = "https://apilayer.com"

        # передаем параметры через словарь params (to, from, amount)
        params = {"to": "RUB", "from": currency_code, "amount": amount}

        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
            response.raise_for_status()  # вызовет ошибку при 4xx или 5xx статусах

            data = response.json()
            return float(data.get("result", 0.0))

        except (requests.RequestException, ValueError, KeyError):
            # в случае ошибки API возвращаем 0.0
            return 0.0

    return 0.0
