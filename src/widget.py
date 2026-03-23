from masks import get_mask_card_number, get_mask_account


def mask_account_card(data_string: str) -> str:
    """
    Маскирует номер карты или счета, сохраняя тип документа.
    Принимает строку вида 'Visa Platinum 7000792289606361'
    """
    # Разделяем строку на части по пробелам
    parts = data_string.split()

    # Номер всегда последний элемент, название — всё остальное
    number = parts[-1]
    type_name = " ".join(parts[:-1])

    # Проверяем, счет это или карта, и применяем нужную маску
    if type_name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{type_name} {masked_number}"
