import unittest
import datetime as dt
import random

# If the script importing the module is not in a package
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from messages import count_dates_from_messages
from api_models import Message


class TestMessages(unittest.TestCase):

    def test_empty_history(self):
        dates, freq = count_dates_from_messages([])
        self.assertEqual(dates, [])
        self.assertEqual(freq, [])

    def test_dates_and_frequencies(self):
        message = {
            'id': 1,
            'peer_id': 123456,
            'from_id': 123456,
            'text': 'Test message',
            'random_id': 17,
            'important': False
        }

        random.seed(17)
        messages = []
        for n in range(10):
            delta_ts = random.randint(86400, 604800)
            ts = int(1543611600 + delta_ts * random.choice([1, -1]))
            date = {'date': ts}
            messages.append(Message(**{**message, **date}))

        dates, freq = count_dates_from_messages(messages)
        self.assertEqual(sorted(freq), [1, 1, 1, 2, 2, 3])
        self.assertEqual(set(dates), {
            dt.date(2018, 11, 24),
            dt.date(2018, 11, 25),
            dt.date(2018, 11, 26),
            dt.date(2018, 11, 28),
            dt.date(2018, 12, 2),
            dt.date(2018, 12, 3)
        })
