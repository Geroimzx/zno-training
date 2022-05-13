from datetime import datetime, time
import pytz


def current_time():
    tz_ua = pytz.timezone('Europe/Kiev')
    now = datetime.now(tz_ua)
    naive_time = datetime.combine(now, time(int(now.hour), int(now.minute), int(now.second)))
    return naive_time