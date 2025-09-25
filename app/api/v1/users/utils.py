from datetime import datetime, date
import json

def str_in_dict_or_error_log(data: str) -> dict | None:
    try:
        payload = json.loads(data)
    except json.JSONDecodeError:
        print(f"Ошибка в пришли некорректные данные, не JSON: {data}")
        return None
    return payload

def str_in_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("Дата должна быть в формате dd/mm/YYYY")