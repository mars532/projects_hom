from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterable, List


def _parse_iso8601(value: str) -> datetime:
    """
    Безопасно парсит ISO 8601 строку вида:
    - 'YYYY-MM-DDTHH:MM:SS'
    - 'YYYY-MM-DDTHH:MM:SS.ffffff'
    - допускает 'Z' и оффсеты '±HH:MM' (отрезаем их для сортировки).
    """
    s = value.strip()
    if s.endswith("Z"):
        s = s[:-1]
    # отрезаем смещение таймзоны, если есть (например, '+03:00' или '-05:00')
    if len(s) >= 6 and (s[-6] in "+-") and s[-3] == ":" and s[-5:-3].isdigit() and s[-2:].isdigit():
        s = s[:-6]

    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue

    # запасной вариант: бросаем информативную ошибку
    raise ValueError(f"Некорректный формат даты: {value!r}")


def filter_by_state(operations: Iterable[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Возвращает новый список операций, оставляя только элементы с указанным статусом.

    Args:
        operations: итерируемое из словарей операций (ожидается ключ 'state').
        state: значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').

    Returns:
        Новый list с операциями, где op.get('state') == state.

    Пример:
        >>> filter_by_state([{'state': 'EXECUTED'}, {'state': 'CANCELED'}])
        [{'state': 'EXECUTED'}]
    """
    return [op for op in operations if isinstance(op, dict) and op.get("state") == state]


def sort_by_date(operations: Iterable[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует операции по ключу 'date'.

    Args:
        operations: итерируемое из словарей операций (ожидается строковый ключ 'date').
        descending: порядок сортировки; True — по убыванию (сначала самые новые).

    Returns:
        Новый list, отсортированный по дате.

    Пример:
        >>> sort_by_date([{'date': '2019-01-02T00:00:00'}, {'date': '2018-01-02T00:00:00'}])
        [{'date': '2019-01-02T00:00:00'}, {'date': '2018-01-02T00:00:00'}]
    """
    def keyfunc(op: Dict[str, Any]) -> datetime:
        value = op.get("date")
        if not isinstance(value, str):
            raise ValueError("Каждая операция должна иметь строковый ключ 'date'")
        return _parse_iso8601(value)

    return sorted(list(operations), key=keyfunc, reverse=descending)
