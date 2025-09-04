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