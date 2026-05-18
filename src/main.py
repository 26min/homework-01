"""Главный модуль приложения для анализа и фильтрации банковских транзакций."""
from src.generators import filter_by_currency
from src.masks import get_mask_account, get_mask_card_number
from src.utils import (
    get_financial_transactions,
    get_transactions_from_csv,
    get_transactions_from_excel,
    process_bank_search
)


def format_account_or_card(data_str: str) -> str:
    """Определяет тип источника/назначения и маскирует его номер."""
    if not data_str:
        return ""

    # Отделяем текстовую часть от цифровой
    parts = data_str.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower() == "счет":
        return f"Счет {get_mask_account(number)}"
    return f"{name} {get_mask_card_number(number)}"


def main() -> None:
    """Отвечает за основную логику проекта и связывает её компоненты."""
    print("Привет! Добро пожаловать в программу работы")
    print("с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    user_choice = input("\nПользователь: ").strip()
    transactions = []

    if user_choice == "1":
        print("\nПрограмма: Для обработки выбран JSON-файл.")
        transactions = get_financial_transactions("data/operations.json")
    elif user_choice == "2":
        print("\nПрограмма: Для обработки выбран CSV-файл.")
        transactions = get_transactions_from_csv("data/operations.csv")
    elif user_choice == "3":
        print("\nПрограмма: Для обработки выбран XLSX-файл.")
        transactions = get_transactions_from_excel("data/operations.xlsx")
    else:
        print("\nПрограмма: Некорректный пункт меню. Перезапустите программу.")
        return

    # Шаг 1: Фильтрация по статусу
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("\nПользователь: ").strip().upper()

        if status_input in valid_statuses:
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{status_input}"')
            transactions = [t for t in transactions if str(t.get("state")).upper() == status_input]
            break
        print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    # Шаг 2: Сортировка по дате
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    sort_choice = input("\nПользователь: ").strip().lower()

    if sort_choice == "да":
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?")
        order_choice = input("\nПользователь: ").strip().lower()

        reverse_order = True if "убывание" in order_choice else False
        # Сортируем по строке даты
        transactions.sort(key=lambda t: t.get("date", ""), reverse=reverse_order)

    # Шаг 3: Фильтрация по валюте (только RUB)
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    rub_choice = input("\nПользователь: ").strip().lower()

    if rub_choice == "да":
        # Используем filter_by_currency
        transactions = list(filter_by_currency(transactions, "RUB"))

    # Шаг 4: Фильтрация по ключевому слову в описании
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    search_choice = input("\nПользователь: ").strip().lower()

    if search_choice == "да":
        search_word = input("\nПользователь: ").strip()
        # Используем функцию поиска с re
        transactions = process_bank_search(transactions, search_word)

    # Шаг 5: Вывод результатов
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for t in transactions:
        # Извлекаем и форматируем дату
        raw_date = t.get("date", "")
        formatted_date = ""
        if len(raw_date) >= 10:
            year, month, day = raw_date[0:4], raw_date[5:7], raw_date[8:10]
            formatted_date = f"{day}.{month}.{year}"

        description = t.get("description", "Описание отсутствует")

        # Маскируем отправителя и получателя
        from_info = format_account_or_card(t.get("from", ""))
        to_info = format_account_or_card(t.get("to", ""))

        route = f"{from_info} -> {to_info}" if from_info else to_info

        # Извлекаем сумму и валюту из структуры operationAmount
        amount_data = t.get("operationAmount", {})
        amount = amount_data.get("amount", 0)
        currency_name = amount_data.get("currency", {}).get("name", "руб.")

        # Вывод операции по шаблону
        print(f"{formatted_date} {description}")
        print(route)
        print(f"Сумма: {amount} {currency_name}\n")


if __name__ == "__main__":
    main()
