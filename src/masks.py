"""Реализуйте в этом модуле две функции:
Функцию маскировки номера банковской карты
get_mask_card_number
Функцию маскировки номера банковского счета
get_mask_account
"""

import logging
import os

# настройка пути: файл masks.log в папке logs в корне проекта
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "masks.log")

# настройка логера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# настройка обработчика файла с перезаписью (mode='w')
file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция для получения ввода номера карты, возвращает маску"""
    # мы берём последние четыре цифры и возвращаем 2 первые цифры
    new_card_number = card_number.replace(" ", "")  # при вводе номера карты есть пробелы, убираем их replace
    if len(new_card_number) != 16:
        return "Вы ввели неверный номер карты, он должен содержать 16 цифр."  # проверяем длину

    if not new_card_number.isdigit():
        return "Вы ввели неверный формат номера карты."  # проверяем на наличие букв/других символов

    new_format_to_return = (
        new_card_number[:4] + " " + new_card_number[4:6] + "**" + " " + "****" + " " + new_card_number[-4:]
    )
    return new_format_to_return


# input_from_user = input("Введите свой номер карты: ")
# returned_value = get_mask_card_number(input_from_user)
# print(returned_value)


def get_mask_account(account_number: str) -> str:
    """Функция для получения ввода номера счета, возвращает маску"""
    new_account_number = account_number.replace(" ", "")  # при вводе мб пробелы, на всякий случай убираем их replace
    if len(new_account_number) != 20:
        return "Вы ввели неверный номер счета, он должен содержать 20 цифр."  # проверяем длину

    if not new_account_number.isdigit():
        return "Вы ввели неверные данные, номер содержит только цифры."  # проверяем на наличие букв/других символов

        # Если проверки пройдены, код дойдет до этой строки:
    return f"**{new_account_number[-4:]}"


# input_from_user_account = input("Введите свой номер счета:")
# returned_value = get_mask_account(input_from_user_account)
# print(returned_value)
