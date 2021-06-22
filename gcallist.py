from src.calendar_service import CalendarService
import sys


def main(accountName):
    CalendarService(accountName).printCalendars()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(
            f"Usage python3 gcallist accountName")

    main(sys.argv[1])
    ## Pass as first an single argument the ID of your client calendar visible from your TW account
    ## use  target.printCalendars() to see all your calendars and find out this id.
