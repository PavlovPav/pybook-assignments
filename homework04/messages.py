from collections import Counter
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple
from typing import Dict
import json

from api import messages_get_history
from api_models import Message
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    date_count: Dict[datetime.date, int] = {}
    for msg in messages:
        if msg.date in date_count:
            print("exists:", msg.date)
            date_count[msg.date] += 1
        else:
            print("new:", msg.date)
            date_count[msg.date] = 1
    dates: Dates = []
    freqs: Frequencies = []
    for date, freq in date_count.items():
        dates.append(date)
        freqs.append(freq)
    return dates, freqs


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly

    :param dates: список дат
    :param freq: число сообщений в соответствующую дату
    """

    data = [go.Scatter(x=dates, y=freq)]
    py.iplot(data)