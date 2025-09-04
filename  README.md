# Masking Utils

Утилиты для маскирования платёжных реквизитов.

## Возможности
- `get_mask_card_number(card_number: str) -> str`  
  Принимает номер карты и возвращает маску формата: `XXXX XX** **** XXXX`.  
  Поддерживается только 16-значный номер (PAN). Пробелы и дефисы в исходной строке допускаются.

- `get_mask_account(account_number: str) -> str`  
  Принимает номер счёта и возвращает маску формата: `**XXXX` (последние 4 цифры).

## Примеры
```python
from masking import get_mask_card_number, get_mask_account

print(get_mask_card_number("1234 5678 9876 5432"))  # 1234 56** **** 5432
print(get_mask_account("40817810099910004312"))     # **4312

# Виджет банковских операций

Мини-пакет с утилитами для обработки и отображения банковских операций клиента.

## Цель
- Отфильтровать операции по состоянию (`state`)
- Отсортировать операции по дате (`date`) с поддержкой ISO 8601

# использование
from src.processing import filter_by_state, sort_by_date

data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
]

# Фильтрация
executed = filter_by_state(data)  # state='EXECUTED' по умолчанию
canceled = filter_by_state(data, 'CANCELED')

# Сортировка (по убыванию — сначала последние операции)
sorted_desc = sort_by_date(data)  # descending=True по умолчанию
sorted_asc = sort_by_date(data, descending=False)

#Ожидаемые результаты
python

executed ==
[
  {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
  {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
]

canceled ==
[
  {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
  {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
]

sorted_desc ==
[
  {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
  {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
  {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
  {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
]