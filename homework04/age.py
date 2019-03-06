import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
#from api_models import User
import datetime
import statistics


def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
    response = get_friends(user_id, 'bdate')
    bh_dates = list()
    u_ages = list()
    for i in range(response.json()['response']['count']):
        friend = response.json()['response']['items'][i]
        if 'bdate' not in friend:
            continue
        try:
            bh_date = datetime.datetime.strptime(friend['bdate'], '%d.%m.%Y')
            u_ages.append(calculate_age(bh_date))
        except ValueError:
            continue
    bh_dates.sort()
    return statistics.median(u_ages)

