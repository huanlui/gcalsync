from src.date_period import DatePeriod
from src.calendar import Calendar
import sys


def main(sourceAccountName, sourceCalendarId, targetAccountName, targetCalendarId, datePeriod, copySensibleData):
    print(f'Copying from {sourceAccountName}:{sourceCalendarId} to {targetAccountName}:{targetCalendarId}'
          f' from {datePeriod.start} to {datePeriod.end}')
    if copySensibleData:
        print('WARNING: copying full inforation from the event. Make sure sensible data is not copied to your new calendar!!')

    sourceCalendar = Calendar(sourceAccountName, sourceCalendarId)
    targetCalendar = Calendar(targetAccountName, targetCalendarId)

    targetCalendar.copyAllEventsFrom(sourceCalendar, DatePeriod.weeks(1), copySensibleData)

    print('Events copied successfully')


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print(
            f"Usage python3 gcalsync sourceAccountName sourceCalendarId targetAccountName targetCalendarId [copySensibleData]")

    copySensibleData = len(sys.argv) > 6 and sys.argv[6] == 'copySensibleData'

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], DatePeriod.parse(sys.argv[5]), copySensibleData)
    ## Pass as first an single argument the ID of your client calendar visible from your TW account
    ## use  target.printCalendars() to see all your calendars and find out this id.
