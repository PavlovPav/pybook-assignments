from typing import List, Optional
from pydantic import BaseModel
import datetime

class BaseUser(BaseModel):
    """ Модель пользователя с базовыми полями """
    id: int
    first_name: str
    last_name: str
    online: int
    deactivated: Optional[str]


class User(BaseUser):
    """ Модель пользователя с необязательным полем дата рождения """
    bdate: Optional[str]


class Message:
    """ Модель сообщения """

    date: datetime.date

    def __init__(self, date):
        self.date = date
