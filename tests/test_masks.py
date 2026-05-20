from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_valid():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_card_number_invalid():
    error_msg = 'Вы ввели неверный номер карты, он должен содержать 16 цифр.'
    assert get_mask_card_number("") == error_msg
    assert get_mask_card_number("12345") == error_msg


def test_get_mask_account_valid():
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_short():
    error_msg = 'Вы ввели неверный номер счета, он должен содержать 20 цифр.'
    assert get_mask_account("123") == error_msg
