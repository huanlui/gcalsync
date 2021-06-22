from src.date_period import DatePeriod
from src.calendar import Calendar
import sys


def main(sourceAccountName, sourceCalendarId, targetAccountName, targetCalendarId):
    sourceCalendar = Calendar(sourceAccountName, sourceCalendarId)
    targetCalendar = Calendar(targetAccountName, targetCalendarId)

    targetCalendar.copyAllEventsFrom(sourceCalendar, DatePeriod.weeks(1))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(f"Usage python3 gcalsync sourceAccountName sourceCalendarId targetAccountName targetCalendarId")

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    ## Pass as first an single argument the ID of your client calendar visible from your TW account
    ## use  twCalendar.printCalendars() to see all your calendars and find out this id.
