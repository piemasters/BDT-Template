import datetime
import time


class TimeManager:

    @staticmethod
    def check_timestamp_recent(timestamp, age):
        """ Checks if a given timestamp is less than x minutes old

        :param timestamp: the timestamp to age
        :param age: the value in minutes to compare the timestamp age against
        :return: True if timestamp is more recent than age passed
        """
        time_val = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        now = datetime.datetime.now()
        if now > time_val:
            return (now - time_val).seconds < 60 * age
        else:
            return (time_val - now).seconds < 60 * age

    @staticmethod
    def timer(duration):
        time.sleep(duration)
