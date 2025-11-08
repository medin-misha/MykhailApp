class APIKeyException(Exception):
    """Ошибка валидации API ключа"""
    def __init__(self, detail: str = "API key is not valid", status_code=400):
        self.detail = detail
        self.status_code = status_code
