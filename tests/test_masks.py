from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_valid():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_card_number_invalid():
    error_msg = 'Вы ввели неверный номер карты, он должен содержать 16 цифр.'
    assert get_mask_card_number("") == error_msg
    assert get_mask_card_number("12345") == error_msg

    # проверяем буквы в номере (длина 16, без цифр)
    error_format_msg = "Вы ввели неверный формат номера карты."
    assert get_mask_card_number("123456781234567a") == error_format_msg

def test_get_mask_account_valid():
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_short():
    error_msg = 'Вы ввели неверный номер счета, он должен содержать 20 цифр.'
    assert get_mask_account("123") == error_msg

def test_get_mask_account_invalid():
    error_msg_len = "Вы ввели неверный номер счета, он должен содержать 20 цифр."
    error_msg_digit = "Вы ввели неверные данные, номер содержит только цифры."

    # Проверяем неверную длину
    assert get_mask_account("12345") == error_msg_len

    # Проверяем буквы вместо цифр
    assert get_mask_account("73654108430135874abc") == error_msg_digit


