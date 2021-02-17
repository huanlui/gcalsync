from datetime import datetime, timezone, timedelta, time
from dataclasses import dataclass
import pytz

@dataclass
class DatePeriod:
    start: str
    end: str

def starting_from_now_for_days(days):
    return DatePeriod(format_to_utc(datetime.utcnow()), format_to_utc(get_end_of_day() + timedelta(days=days - 1)))

def starting_from_now_for_weeks(weeks):
    return DatePeriod(format_to_utc(datetime.utcnow()), format_to_utc(get_end_of_week() + timedelta(weeks=weeks - 1)))

def format_to_utc(datetime):
    return datetime.isoformat().replace('+00:00','') + 'Z'

def get_end_of_day():
    today = datetime.utcnow()

    start = datetime(today.year, today.month, today.day).astimezone(pytz.utc)
    end = start + timedelta(days=1) - timedelta(microseconds=1)
    return end

def get_end_of_week():
    end_of_day = get_end_of_day() 
    start = end_of_day - timedelta(days=end_of_day.weekday())
    end = start + timedelta(days=6) - timedelta(seconds=1)
    return end