from typing import Final

CARD_LENGTH: Final[int] = 16


def _only_digits(value: str) -> str:
    """Возвращает строку, оставляя только цифры."""
    return "".join(ch for ch in value if ch.isdigit())


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Требования ТЗ:
    - На вход — номер карты.
    - На выход — маска вида: 'XXXX XX** **** XXXX'
      (показываем первые 6 и последние 4 цифры, остальное скрыто).
    - Поддерживаем только 16-значные PAN.

    Пример:
    '1234 5678 9876 5432' -> '1234 56** **** 5432'
    """
    digits = _only_digits(card_number)

    if len(digits) != CARD_LENGTH:
        raise ValueError("Некорректный номер карты: требуется 16 цифр")

    # Формат строго по ТЗ: 'XXXX XX** **** XXXX'
    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


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


if __name__ == "__main__":
    card = "1234 5678 9876 5432"
    account = "40817810099910004312"

    print("Маска карты:", get_mask_card_number(card))  # 1234 56** **** 5432
    print("Маска счёта:", get_mask_account(account))  # **4312
