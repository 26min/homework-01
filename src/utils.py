import json
import os
import logging

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

def get_financial_transactions(path):
    """
    читает json и возвращает список словарей
    возвращает пустой список, если файл не найден, пуст или содержит не список.
    """

    logger.info(f"Попытка открытия файла: {path}")

    if not os.path.exists(path):
        logger.error(f"Файл не найден: {path}")
        return []

    try:
        with open(path, 'r', encoding='utf-8') as f:
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


