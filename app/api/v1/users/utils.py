import json

def str_in_dict_or_error_log(data: str) -> dict | None:
    try:
        payload = json.loads(data)
    except json.JSONDecodeError:
        print(f"Ошибка в пришли некорректные данные, не JSON: {data}")
        return None
    return payload