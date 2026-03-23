import re
from masks import get_mask_card_number, get_mask_account


def mask_account_card(data_str: str) -> str:
    """
    Универсальная функция: определяет тип (карта/счет) и отправляет в нужную маску только цифры
    """

    numbers_only = "".join(re.findall(r"\d+", data_str)) # извлекаем только цифры

    type_name = "".join(re.findall(r"\D+", data_str)).strip() # извлекаем только текст


    if "счет" in type_name.lower():            # если будет ключевое слово "счет", то примениться маска для счета,
        masked_number = get_mask_account(numbers_only)   # если не будет ключевого слова, то применится маска
                                                                         # для номера карты
    else:
        masked_number = get_mask_card_number(numbers_only)

    return f"{type_name} {masked_number}"


if __name__ == "__main__":
    user_input = input("Введите данные: ")
    print(mask_account_card(user_input))
