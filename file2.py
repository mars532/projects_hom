from __future__ import annotations

from typing import Final
from datetime import datetime
import re

CARD_LENGTH: Final[int] = 16


def _only_digits(value: str) -> str:
    """Возвращает строку, оставляя только цифры."""
    return "".join(ch for ch in value if ch.isdigit())


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты (только 16-значные PAN).

    Формат: 'XXXX XX ** XXXX' — первые 6 и последние 4 цифры видны.
    """
    digits = _only_digits(card_number)
    if len(digits) != CARD_LENGTH:
        raise ValueError("Некорректный номер карты: требуется 16 цифр")
    return f"{digits[:4]} {digits[4:6]} ** {digits[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта.

    Формат: '**XXXX' — две звёздочки + последние 4 цифры.
    """
    digits = _only_digits(account_number)
    if len(digits) < 4:
        raise ValueError("Некорректный номер счёта: минимум 4 цифры")
    return f"**{digits[-4:]}"


def mask_account_card(info: str) -> str:
    """
    Маскирует номер карты или счёта в зависимости от типа строки.

    Примеры:
      "Visa Platinum 7000792289606361"   -> "Visa Platinum 7000 79 ** 6361"
      "Счёт 73654108430135874305"       -> "Счёт **4305"
      "MasterCard 1234 5678 9876 5432"  -> "MasterCard 1234 56 ** 5432"
      "Account № 40817810099910004312"  -> "Account № **4312"
    """
    if not info or not info.strip():
        raise ValueError("Пустая строка: ожидалась информация вида 'Тип Номер'")

    s = " ".join(info.split()).strip()

    # Берём последнюю числовую группу (допускаем пробелы внутри номера)
    m = re.search(r"(\d[\d ]+)$", s)
    if not m:
        raise ValueError("Не найден числовой идентификатор в конце строки")

    number_raw = m.group(1)
    card_type = s[: m.start(1)].strip()

    t = card_type.lower()
    is_card = any(
        key in t
        for key in (
            "карта", "visa", "maestro", "mastercard", "master card",
            "mir", "american express", "amex", "electron"
        )
    )
    is_account = any(key in t for key in ("счет", "счёт", "account", "acct"))

    if is_card:
        return f"{card_type} {get_mask_card_number(number_raw)}"
    if is_account:
        return f"{card_type} {get_mask_account(number_raw)}"

    # Фолбэк по длине, если тип явно не указан
    digits = _only_digits(number_raw)
    if len(digits) == CARD_LENGTH:
        return f"{card_type} {get_mask_card_number(number_raw)}"
    if len(digits) >= 4:
        return f"{card_type} {get_mask_account(number_raw)}"

    raise ValueError("Неизвестный тип информации и/или некорректная длина номера")


def get_date(date_string: str) -> str:
    """
    Преобразует дату из ISO 8601 в 'DD.MM.YYYY'.

    Поддерживает:
      - 'YYYY-MM-DDTHH:MM:SS'
      - 'YYYY-MM-DDTHH:MM:SS.ffffff'
      - с суффиксом 'Z' или смещением таймзоны '±HH:MM'
      - 'YYYY-MM-DD'
    """
    if not date_string or not isinstance(date_string, str):
        raise ValueError("Ожидается непустая строка с датой")

    s = date_string.strip()
    # Отбрасываем суффикс таймзоны вида Z или ±HH:MM, если он есть
    s = re.sub(r"(Z|[+-]\d{2}:\d{2})$", "", s)

    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            pass

    # (необязательно) запасной вариант — если прилетит редкий ISO-вариант
    try:
        dt = datetime.fromisoformat(s)
        return dt.strftime("%d.%m.%Y")
    except Exception as e:  # noqa: BLE001
        raise ValueError(
            "Некорректная дата: ожидаю ISO 8601 вида "
            "'YYYY-MM-DD[THH:MM:SS[.ffffff]][Z|±HH:MM]'"
        ) from e


if __name__ == "__main__":
    card_data = "Visa Platinum 7000792289606361"
    account_data = "Счет 73654108430135874305"

    print("Карта:", mask_account_card(card_data))    # Visa Platinum 7000 79 ** 6361
    print("Счёт:", mask_account_card(account_data))  # Счет **4305
    print("Дата:", get_date("2018-07-11T02:26:18.671407"))  # 11.07.2018
