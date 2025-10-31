from argon2 import PasswordHasher, Type
from argon2.exceptions import VerificationError, VerifyMismatchError

HASHER = PasswordHasher(
    time_cost=3,
    memory_cost=64 * 1024,
    parallelism=2,
    hash_len=32,
    salt_len=16,
    type=Type.ID
)

def hash_password(plain_password: str) -> str:
    """
    Превращение пароля в безопасный хеш.
    - Соль генерируеться автоматически и вшываеться в результат
    - Параметры и ти алгоритма так же вшиваються
    Возвращает строку типа:  $argon2id$v=19$m=65536,t=3,p=2$<salt>$<hash>
    """
    if not isinstance(plain_password, str) or not plain_password:
        raise ValueError("Пароль должен быть непустой строкой.")
    return HASHER.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль против хэша
    Возвращает True\False.
    Если исключение возвращаем False
    """
    try:
        return HASHER.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, Exception):
        return False