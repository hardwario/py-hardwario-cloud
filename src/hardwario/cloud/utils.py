import time
from datetime import datetime, tzinfo
from dateutil.parser import parse
from dateutil.tz import tzlocal


def get_timestamp(value):
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    d = parse(value)
    return int(time.mktime(d.timetuple()) * 1000)
