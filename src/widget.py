import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data_str: str) -> str:
    """
    Универсальная функция: определяет тип (карта/счет) и отправляет в нужную маску только цифры
    """

    numbers_only = "".join(re.findall(r"\d+", data_str))  # извлекаем только цифры

    type_name = "".join(re.findall(r"\D+", data_str)).strip()  # извлекаем только текст

    if "счет" in type_name.lower():  # если будет ключевое слово "счет", то применится маска для счета,
        masked_number = get_mask_account(numbers_only)  # если не будет, то применится маска для номера карты
    else:
        masked_number = get_mask_card_number(numbers_only)

    return f"{type_name} {masked_number}"


if __name__ == "__main__":
    user_input = input("Введите данные: ")
    print(mask_account_card(user_input))


def get_date(date_string: str) -> str:
    """
    Преобразует строку "2024-03-11T02:26:18.671407" с помощью срезов.
    """

    year = date_string[0:4]  # извлекаем год

    month = date_string[5:7]  # извлекаем месяц

    day = date_string[8:10]  # извлекаем день

    return f"{day}.{month}.{year}"  # собираем в нужном порядке через точку


test_date = "2024-03-11T02:26:18.671407"
print(f"Дата: {get_date(test_date)}")
