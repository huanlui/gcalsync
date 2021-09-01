from src.date_period import DatePeriod
from src.calendar_service import CalendarService
import sys
import argparse


def main(sourceAccountName, sourceCalendarId, targetAccountName, targetCalendarId, datePeriod, copySensibleData, colorId, skipMatching):
    print(f'Copying from {sourceAccountName}:{sourceCalendarId} to {targetAccountName}:{targetCalendarId}'
          f' from {datePeriod.start} to {datePeriod.end}')
    if copySensibleData:
        print('WARNING: copying full inforation from the event. Make sure sensible data is not copied to your new calendar!!')

    sourceCalendar = CalendarService(sourceAccountName).getCalendar(sourceCalendarId)
    targetCalendar = CalendarService(targetAccountName).getCalendar(targetCalendarId)

    targetCalendar.copyAllEventsFrom(sourceCalendar, datePeriod, copySensibleData, colorId, skipMatching)

    print('Events copied successfully')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This command copies event from a source calendar to a target one.')
    parser.add_argument('sourceAccountName', type=str, help='Name of the source account (credentials file prefix)')
    parser.add_argument('sourceCalendarId', type=str, help='Name of the source calendar (use `gcallist` to find)')
    parser.add_argument('targetAccountName', type=str, help='Name of the target account (credentials file prefix)')
    parser.add_argument('targetCalendarId', type=str, help='Name of the source calendar (use `gcallist` to find)')
    parser.add_argument('period', type=str, help='Period of events to copy, e.g. 2d or 1w')
    parser.add_argument('--copySensibleData', action='store_true', help='If set, copies event names and details')
    parser.add_argument('--colorId', type=str, default=None, help='If set, uses custom color (see `colors` resource)')
    parser.add_argument('--skipMatching', action='store_true', help='If set, does not copy events if there already exists an event in the target calendar with the same start and end time')

    args = parser.parse_args()
    main(args.sourceAccountName, args.sourceCalendarId, args.targetAccountName, args.targetCalendarId, DatePeriod.parse(args.period), args.copySensibleData, args.colorId, args.skipMatching)
    ## Pass as first an single argument the ID of your client calendar visible from your TW account
    ## use  target.printCalendars() to see all your calendars and find out this id.
