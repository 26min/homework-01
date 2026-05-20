# """Модуль автоматического тестирования финансовых утилит и внешних API."""
# import unittest
# from unittest.mock import mock_open, patch
#
# import pandas as pd
# import requests
#
# from src.external_api import convert_to_rub
# from src.utils import get_financial_transactions, get_transactions_from_csv, get_transactions_from_excel
#
#
# class TestFinancialApp(unittest.TestCase):
#     """Набор тестов для проверки утилит и интеграции с внешним API."""
#
#     # тесты для модуля utils (JSON)
#
#     @patch("os.path.exists")
#     @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}]')
#     def test_get_transactions_success(self, mock_file, mock_exists):
#         """Тест успешного получения данных из json."""
#         mock_exists.return_value = True
#         result = get_financial_transactions("data/operations.json")
#         self.assertEqual(result, [{"id": 1}])
#
#     @patch("os.path.exists")
#     def test_get_transactions_file_not_found(self, mock_exists):
#         """Тест, когда файл не найден."""
#         mock_exists.return_value = False
#         result = get_financial_transactions("non_existent.json")
#         self.assertEqual(result, [])
#
#     @patch("os.path.exists")
#     @patch("builtins.open", new_callable=mock_open, read_data="")
#     def test_get_transactions_empty_file(self, mock_file, mock_exists):
#         """Тест пустого файла -> вернуть пустой список."""
#         mock_exists.return_value = True
#         result = get_financial_transactions("empty.json")
#         self.assertEqual(result, [])
#
#     @patch("os.path.exists")
#     @patch("builtins.open", new_callable=mock_open, read_data='{"not_a_list": 1}')
#     def test_get_transactions_not_a_list(self, mock_file, mock_exists):
#         """Тест файла, где вместо списка идет словарь."""
#         mock_exists.return_value = True
#         result = get_financial_transactions("wrong_format.json")
#         self.assertEqual(result, [])
#
#     # новые тесты для модуля utils - CSV и Excel через Pandas
#
#     @patch("os.path.exists")
#     @patch("pandas.read_csv")
#     def test_get_transactions_from_csv_success(self, mock_read_csv, mock_exists):
#         """Тест успешного чтения CSV через подмену DataFrame."""
#         mock_exists.return_value = True
#         fake_df = pd.DataFrame([{"id": 123, "amount": 500}])
#         mock_read_csv.return_value = fake_df
#
#         result = get_transactions_from_csv("dummy.csv")
#         self.assertEqual(result, [{"id": 123, "amount": 500}])
#
#     @patch("os.path.exists")
#     def test_get_transactions_from_csv_file_not_found(self, mock_exists):
#         """Тест ситуации, когда CSV файл отсутствует на диске."""
#         mock_exists.return_value = False
#         result = get_transactions_from_csv("missing.csv")
#         self.assertEqual(result, [])
#
#     @patch("os.path.exists")
#     @patch("pandas.read_excel")
#     def test_get_transactions_from_excel_success(self, mock_read_excel, mock_exists):
#         """Тест успешного чтения Excel через подмену DataFrame."""
#         mock_exists.return_value = True
#         fake_df = pd.DataFrame([{"id": 456, "amount": 1000}])
#         mock_read_excel.return_value = fake_df
#
#         result = get_transactions_from_excel("dummy.xlsx")
#         self.assertEqual(result, [{"id": 456, "amount": 1000}])
#
#     @patch("os.path.exists")
#     def test_get_transactions_from_excel_file_not_found(self, mock_exists):
#         """Тест ситуации, когда Excel файл отсутствует на диске."""
#         mock_exists.return_value = False
#         result = get_transactions_from_excel("missing.xlsx")
#         self.assertEqual(result, [])
#
#     # тесты для external_api
#
#     def test_convert_rub_directly(self):
#         """Тест: RUB не должен конвертироваться через API."""
#         transaction = {
#             "operationAmount": {
#                 "amount": "100.50",
#                 "currency": {"code": "RUB"}
#             }
#         }
#         self.assertEqual(convert_to_rub(transaction), 100.50)
#
#     @patch("requests.get")
#     def test_convert_usd_via_api(self, mock_get):
#         """Тест конвертации USD через mock к API."""
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.json.return_value = {"result": 7500.0}
#
#         transaction = {
#             "operationAmount": {
#                 "amount": "100",
#                 "currency": {"code": "USD"}
#             }
#         }
#
#         result = convert_to_rub(transaction)
#
#         # проверяем корректность возвращаемой суммы
#         self.assertEqual(result, 7500.0)
#
#         # проверяем, что параметры запроса сформированы верно
#         args, kwargs = mock_get.call_args
#         self.assertEqual(kwargs["params"]["to"], "RUB")
#         self.assertEqual(kwargs["params"]["from"], "USD")
#
#     @patch("requests.get")
#     def test_convert_api_error_returns_zero(self, mock_get):
#         """Тест: при сбое сети API должен возвращаться 0.0."""
#         mock_get.side_effect = requests.exceptions.RequestException
#
#         transaction = {
#             "operationAmount": {
#                 "amount": "100",
#                 "currency": {"code": "USD"}
#             }
#         }
#
#         result = convert_to_rub(transaction)
#         self.assertEqual(result, 0.0)
#
#
# if __name__ == "__main__":
#     unittest.main()
from unittest.mock import MagicMock, patch

# import pytest
import requests

from src.external_api import convert_to_rub


def test_convert_to_rub_currency() -> None:
    """Тест конвертации, если валюта изначально является RUB."""
    transaction = {
        "operationAmount": {
            "amount": "1500.50",
            "currency": {"name": "рубль", "code": "RUB"}
        }
    }
    assert convert_to_rub(transaction) == 1500.50


@patch("src.external_api.requests.get")
def test_convert_to_rub_usd_success(mock_get: MagicMock) -> None:
    """Тест успешного запроса к API для конвертации USD в RUB."""
    # Имитируем успешный ответ от API сервера apilayer.com
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 7500.0}
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100.0",
            "currency": {"name": "доллар", "code": "USD"}
        }
    }

    result = convert_to_rub(transaction)

    assert result == 7500.0
    mock_get.assert_called_once()

    # Извлекаем переданные в запросе аргументы
    called_args, called_kwargs = mock_get.call_args
    assert called_args[0] == "https://apilayer.com"
    assert called_kwargs["params"] == {"to": "RUB", "from": "USD", "amount": 100.0}
    assert called_kwargs["timeout"] == 5
    assert "apikey" in called_kwargs["headers"]


@patch("src.external_api.requests.get")
def test_convert_to_rub_api_error(mock_get: MagicMock) -> None:
    """Тест возврата 0.0 при возникновении сетевой ошибки или ошибки сервера."""
    mock_get.side_effect = requests.RequestException("Ошибка подключения")

    transaction = {
        "operationAmount": {
            "amount": "100.0",
            "currency": {"name": "евро", "code": "EUR"}
        }
    }

    assert convert_to_rub(transaction) == 0.0


def test_convert_to_rub_unknown_currency() -> None:
    """Тест возврата 0.0 для неподдерживаемой кодом валюты (например, GBP)."""
    transaction = {
        "operationAmount": {
            "amount": "50.0",
            "currency": {"name": "фунт", "code": "GBP"}
        }
    }
    assert convert_to_rub(transaction) == 0.0
