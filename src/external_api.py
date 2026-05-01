import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")


def convert_to_rub(transaction):
    """
    возвращает сумму транзакции в рублях (float),
    если валюта USD или EUR, запрашивает курс через API.
    """
    amount = float(transaction.get("operationAmount", {}).get("amount", 0))
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if currency == "RUB":
        return amount

    if currency in ["USD", "EUR"]:
        url = f"https://apilayer.com{currency}&amount={amount}"
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            return float(data.get("result", 0))
        except (requests.RequestException, ValueError, KeyError):
            return 0.0

    return 0.0
