 # Виджет банковских операций

Утилиты для фильтрации и сортировки операций.

## Установка
```bash
git clone https://github.com/<user>/<repo>.git
cd <repo>
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # при необходимости
## Использование
python

from src.processing import filter_by_state, sort_by_date

data = [
  {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
  {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
  {"id": 594226727, "state": "CANCELED",  "date": "2018-09-12T21:27:25.241689"},
  {"id": 615064591, "state": "CANCELED",  "date": "2018-10-14T08:21:33.419441"},
]

print(filter_by_state(data))            # по умолчанию state='EXECUTED'
print(filter_by_state(data, "CANCELED"))

print(sort_by_date(data))               # убывание (новые сначала)
print(sort_by_date(data, descending=False))
## Тесты и линтеры
bash

pip install -U pytest flake8 mypy
pytest -q
flake8 .
mypy .
text


# Именование и стиль
- функции/переменные — `snake_case`: `filter_by_state`, `sort_by_date`, `operations`, `descending`;
- константы — `UPPER_SNAKE_CASE`;
- docstring — в стиле *Google* или *reST* (выше показан лаконичный вариант);
- избегаем дублирования кода: в `widget.py` оставляем только **импорты** из `masks` (мы это уже починили ранее).