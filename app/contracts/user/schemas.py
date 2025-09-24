from pydantic import BaseModel, PositiveInt
from datetime import datetime, date

class BaseUser(BaseModel):
    chat_id: PositiveInt
    username: str

class CreateUser(BaseUser):
    pass

class ReturnUser(BaseUser):
    id: str
    last_login_at: datetime
    registered_at: datetime
    birthday_date: date

class ChatId(BaseModel):
    chat_id: PositiveInt