import unittest
from unittest.mock import mock_open, patch
from src.external_api import convert_to_rub
from src.utils import get_financial_transactions


class TestFinancialApp(unittest.TestCase):

    # тесты для utils

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}]')
    def test_get_transactions_success(self, mock_file, mock_exists):
        """тест успешного получения данных из json"""
        mock_exists.return_value = True
        result = get_financial_transactions("data/operations.json")
        self.assertEqual(result, [{"id": 1}])

    @patch("os.path.exists")
    def test_get_transactions_file_not_found(self, mock_exists):
        """тест ситуации, когда файл не найден"""
        mock_exists.return_value = False
        result = get_financial_transactions("non_existent.json")
        self.assertEqual(result, [])

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='')
    def test_get_transactions_empty_file(self, mock_file, mock_exists):
        """тест пустого файла -> должен вернуть пустой список"""
        mock_exists.return_value = True
        result = get_financial_transactions("empty.json")
        self.assertEqual(result, [])

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"not_a_list": 1}')
    def test_get_transactions_not_a_list(self, mock_file, mock_exists):
        """тест файла, где вместо списка идет словарь"""
        mock_exists.return_value = True
        result = get_financial_transactions("wrong_format.json")
        self.assertEqual(result, [])

    # тесты для модуля external_api

    def test_convert_rub_directly(self):
        """тест: RUB не должен конвертироваться через API"""
        transaction = {
            "operationAmount": {
                "amount": "100.50",
                "currency": {"code": "RUB"}
            }
        }
        self.assertEqual(convert_to_rub(transaction), 100.50)

    @patch("requests.get")
    def test_convert_usd_via_api(self, mock_get):
        # настраиваем фейковый ответ
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": 7500.0}

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        result = convert_to_rub(transaction)

        # проверяем, что сумма верная
        assert result == 7500.0

        # проверяем, что параметры переданы правильно
        args, kwargs = mock_get.call_args
        assert kwargs['params']['to'] == 'RUB'
        assert kwargs['params']['from'] == 'USD'


if __name__ == "__main__":
    unittest.main()
