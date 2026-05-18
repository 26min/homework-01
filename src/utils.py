"""Модуль для чтения финансовых транзакций из файлов JSON, CSV и Excel."""
import json
import logging
import os

import pandas as pd

# Настройка пути: файл utils.log в папке logs в корне проекта
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "utils.log")

# Настройка логера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Настройка обработчика файла с перезаписью (mode='w')
file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_financial_transactions(path: str) -> list:
    """Читает json и возвращает список словарей.

    Возвращает пустой список, если файл не найден, пуст или содержит не список.
    """
    logger.info(f"Попытка открытия файла: {path}")

    if not os.path.exists(path):
        logger.error(f"Файл не найден: {path}")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info(f"Успешно прочитано транзакций: {len(data)}")
                return data
            else:
                logger.warning(f"Данные в файле {path} не являются списком")
                return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {path}")
        return []
    except UnicodeDecodeError:
        logger.error(f"Ошибка кодировки в файле: {path}")
        return []
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при работе с файлом {path}: {e}")
        return []


def get_transactions_from_csv(path: str) -> list:
    """Читает транзакции из csv-файла с помощью pandas.

    Возвращает список словарей, если файл не найден или пуст - возвращает пустой список.
    """
    logger.info(f"Попытка открытия csv файла: {path}")
    if not os.path.exists(path):
        logger.error(f"csv файл не найден по пути: {path}")
        return []

    try:
        # автоматически определяем разделитель (запятая или точка с запятой)
        df = pd.read_csv(path, sep=None, engine='python')

        # заменяем NaN на None
        df = df.where(pd.notnull(df), None)

        # конвертируем таблицу в привычный список словарей
        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно прочитано {len(transactions)} транзакций из csv")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при обработке csv файла {path}: {e}")
        return []


def get_transactions_from_excel(path: str) -> list:
    """Читает транзакции из Excel-файла с помощью pandas.

    Возвращает список словарей, если файл не найден или пуст - возвращает пустой список.
    """
    logger.info(f"Попытка открытия Excel файла: {path}")
    if not os.path.exists(path):
        logger.error(f"Excel файл не найден по пути: {path}")
        return []

    try:
        # открываем Excel файл через openpyxl
        df = pd.read_excel(path, engine="openpyxl")

        # заменяем пустые ячейки NaN на None
        df = df.where(pd.notnull(df), None)

        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно прочитано {len(transactions)} транзакций из Excel")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при обработке Excel файла {path}: {e}")
        return []
