
# Проект: Виджет банковских операций 

## Описание
Данный проект предназначен для фильтрации и сортировки банковских транзакций. Модуль `processing` содержит инструменты для обработки списков данных по статусу операции и по дате.

## Функциональность модуля `processing`

В модуле реализованы две функции:

1. **`filter_by_state`**
   - Фильтрует транзакции по их статусу.
   - По умолчанию ищет операции со статусом `EXECUTED`.
   - Возвращает новый список словарей.

2. **`sort_by_date`**
   - Сортирует транзакции по дате (от самых новых к самым старым по умолчанию).
   - Позволяет менять порядок сортировки с помощью параметра `reverse`.

## Примеры использования

```python
from processing import filter_by_state, sort_by_date

data = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01T12:00:00'},
    {'id': 2, 'state': 'CANCELED', 'date': '2023-05-01T15:30:00'}
]

# Фильтрация по статусу
executed_ops = filter_by_state(data, state='EXECUTED')

# Сортировка по дате
sorted_ops = sort_by_date(data)
```


# Проект: Маскировка и фильтрация транзакций

## Описание
Этот проект предназначен для работы с банковскими транзакциями, их маскировки и фильтрации.

## Тестирование
Для запуска тестов используйте:
pytest

### Покрытие
Для генерации отчета о покрытии кода:
pytest --cov=src --cov-report=html
Отчет сохранен в папке `htmlcov/`


## Модуль generators

Модуль содержит функции-генераторы для обработки больших массивов данных. 
Генераторы позволяют быстро фильтровать транзакции и генерировать последовательности, не загружая всю память устройства.

### Основные функции и примеры использования:

#### 1. filter_by_currency
Фильтрует список транзакций по заданному коду валюты (`USD`, `RUB` и тд).

```python
from src.generators import filter_by_currency

# итератор с транзакциями в долларах
usd_transactions = filter_by_currency(transactions, "USD")

# выводим первую найденную транзакцию
print(next(usd_transactions))
```
 #### 2. transaction_descriptions
Возвращает описания каждой операции из списка транзакций по очереди.

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)

# Выводим первые 5 описаний
for x in range(5):
    print(next(descriptions))
```

#### 3. card_number_generator
Генерирует номера банковских карт в формате 
XXXX XXXX XXXX XXXX в заданном числовом диапазоне.
```python
from src.generators import card_number_generator

# Генерируем номера в диапазоне от 1 до 5
for card_number in card_number_generator(1, 5):
    print(card_number)
# Результат: 0000 0000 0000 0001 и тд
```