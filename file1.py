from typing import Final
from datetime import datetime

CARD_LENGTH: Final[int] = 16


def _only_digits(value: str) -> str:
    """Возвращает строку, оставляя только цифры."""
    return "".join(ch for ch in value if ch.isdigit())


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Требования ТЗ:
    - На вход — номер карты.
    - На выход — маска вида: 'XXXX XX ** XXXX'
      (показываем первые 6 и последние 4 цифры, остальное скрыто).
    - Поддерживаем только 16-значные PAN.

    Пример:
    '1234 5678 9876 5432' -> '1234 56 ** 5432'
    """
    digits = _only_digits(card_number)

    if len(digits) != CARD_LENGTH:
        raise ValueError("Некорректный номер карты: требуется 16 цифр")

    return f"{digits[:4]} {digits[4:6]} ** {digits[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта.

    Требования ТЗ:
    - На вход — номер счёта.
    - На выход — маска вида: '**XXXX' (две звёздочки + последние 4 цифры).

    Пример:
    '40817810099910004312' -> '**4312'
    """
    digits = _only_digits(account_number)

    if len(digits) < 4:
        raise ValueError("Некорректный номер счёта: минимум 4 цифры")

    return f"**{digits[-4:]}"


def mask_account_card(info: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    Аргумент:
    - info (str): строка с типом и номером. Например, "Visa Platinum 7000792289606361" или "Счет 73654108430135874305".

    Возвращает:
    - str: замаскированный номер.
    """
    parts = info.rsplit(" ", 1)  # Разделяем строку на тип и номер
    card_type = parts[0]
    number = parts[1]

    # Если это номер карты, используем get_mask_card_number
    if any(issuer in card_type.lower() for issuer in ['карта', 'visa', 'maestro', 'mastercard']):
        return f"{card_type} {get_mask_card_number(number)}"

    # Если это счет, используем get_mask_account
    elif 'счет' in card_type.lower():
        return f"{card_type} {get_mask_account(number)}"

    raise ValueError("Неизвестный тип информации")


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата 'YYYY-MM-DDTHH:MM:SS' в 'DD.MM.YYYY'.

    Аргумент:
    - date_string (str): строка с датой.

    Возвращает:
    - str: дата в формате 'DD.MM.YYYY'.
    """
    dt = datetime.fromisoformat(date_string)  # Преобразуем строку в объект datetime
    return dt.strftime("%d.%m.%Y")  # Возвращаем строку в нужном формате


# Примеры использования функций
if __name__ == "__main__":
    # Примеры работы функции mask_account_card
    card_data = "Visa Platinum 7000792289606361"
    account_data = "Счет 73654108430135874305"

    print("Выход функции для карты:", mask_account_card(card_data))  # Ожидаемый вывод: Visa Platinum 7000 79 **
