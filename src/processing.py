from datetime import datetime


def filter_by_state(items: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param items: список словарей с данными
    :param state: значение для фильтрации (по умолчанию 'EXECUTED')
    :return: новый список словарей, соответствующих указанному состоянию
    """
    filtered = []
    for item in items:
        if item.get("state") == state:
            filtered.append(item)
    return filtered


def sort_by_date(items: list[dict], descending: bool = True) -> list[dict]:
    """
    Сортирует список словарей по ключу 'date'.

    :param items: список словарей
    :param descending: порядок сортировки (True — по убыванию, False — по возрастанию)
    :return: новый список словарей, отсортированный по дате
    """
    return sorted(
        items,
        key=lambda x: datetime.fromisoformat(x["date"]),
        reverse=descending
    )


# if __name__ == "__main__":
#     test_data = [
#         {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
#     ]
#
#     # Проверка фильтрации
#     executed_data = filter_by_state(test_data)
#     print("Отфильтрованные (EXECUTED):", executed_data)
#
#     # Проверка сортировки (по умолчанию — самые свежие сверху)
#     sorted_data = sort_by_date(test_data)
#     print("\nОтсортированные по дате (убывание):", sorted_data)
