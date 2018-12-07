import unittest
import datetime

from bdt_template import TimeManager


class TimeManagerTests(unittest.TestCase):

    def test_check_timestamp_recent(self):
        # Create a timestamp that is 5 minutes old
        five_mins_ago = str(datetime.datetime.now() - datetime.timedelta(minutes=5))

        # Check if the timestamp is less than 10 minutes old
        timestamp_age = 10
        result = TimeManager.check_timestamp_recent(five_mins_ago, timestamp_age)

        expected = True

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
