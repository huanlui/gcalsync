from datetime import datetime, timezone, timedelta, time
from dataclasses import dataclass
import pytz

@dataclass
class DatePeriod:
    start: str
    end: str

    @staticmethod
    def days(days):
        return DatePeriod(formatToUtc(datetime.utcnow()), formatToUtc(getEndOfDay() + timedelta(days=days - 1)))

    @staticmethod
    def weeks(weeks):
        return DatePeriod(formatToUtc(datetime.utcnow()), formatToUtc(getEndOfWeek() + timedelta(weeks=weeks - 1)))

def formatToUtc(datetime):
    return datetime.isoformat().replace('+00:00','') + 'Z'

def getEndOfDay():
    today = datetime.utcnow()

    start = datetime(today.year, today.month, today.day).astimezone(pytz.utc)
    end = start + timedelta(days=1) - timedelta(microseconds=1)
    return end

def getEndOfWeek():
    end_of_day = getEndOfDay() 
    start = end_of_day - timedelta(days=end_of_day.weekday())
    end = start + timedelta(days=6) - timedelta(seconds=1)
    return end