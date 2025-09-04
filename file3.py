from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Dict, Any


def _parse_iso_dt(value: str) -> datetime:
    """
    Аккуратно парсит ISO 8601 дату вида 'YYYY-MM-DDTHH:MM:SS[.ffffff]'.

    Допускаем суффиксы 'Z' или смещения таймзоны '±HH:MM' — отбрасываем их
    для целей сортировки по дате.
    """
    s = value.strip()
    # убираем 'Z' или оффсет таймзоны, если есть
    if s.endswith("Z"):
        s = s[:-1]
    if len(s) >= 6 and (s[-6] in "+-") and (s[-3] == ":") and s[-5:-3].isdigit() and s[-2:].isdigit():
        s = s[:-6]

    # пробуем с микросекундами и без
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    # как запасной вариант — просто дата без времени
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты: {value}") from e


def filter_by_state(items: Iterable[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Возвращает новый список словарей, оставляя только элементы с заданным state.

    :param items: список/итерируемое со словарями операций
    :param state: значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED')
    :return: новый список, где item.get('state') == state
    """
    # делаем иммутабельный результат: создаём новый список
    return [op for op in items if isinstance(op, dict) and op.get("state") == state]


def sort_by_date(items: Iterable[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date'.

    :param items: список/итерируемое со словарями операций
    :param descending: порядок сортировки; True — по убыванию (сначала новые)
    :return: НОВЫЙ отсортированный список
    """
    def keyfunc(op: Dict[str, Any]) -> datetime:
        value = op.get("date")
        if not isinstance(value, str):
            raise ValueError("Каждый элемент должен иметь строковый ключ 'date'")
        return _parse_iso_dt(value)

    # создаём копию и сортируем её
    return sorted(list(items), key=keyfunc, reverse=descending)
