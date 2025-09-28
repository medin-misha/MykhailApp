from pydantic import BaseModel, PositiveInt, field_validator
from datetime import datetime, date

class BaseUser(BaseModel):
    chat_id: PositiveInt
    username: str

class CreateUser(BaseUser):
    pass

class ReturnUser(BaseUser):
    id: int
    last_login_at: datetime | None
    registered_at: datetime
    birthday_date: date

class ChatId(BaseModel):
    chat_id: PositiveInt

class BirthdayModel(BaseModel):
    chat_id: int
    birthday: str

    @field_validator("birthday")
    def validate_birthday(cls, value):
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Дата должна быть в формате dd/mm/YYYY")
        return value