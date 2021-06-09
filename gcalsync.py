from src.date_period import DatePeriod
from src.calendar import Calendar
import sys

def main(clientCalendarId):
    twCalendar = Calendar("tw", "primary")
    
    clientCalendar = Calendar("tw", clientCalendarId )

    twCalendar.copyAllEventsFrom(clientCalendar, DatePeriod.weeks(1))

if __name__ == '__main__':
    main(sys.argv[1])
    ## Pass as first an single argument the ID of your client calendar visible from your TW account
    ## use  twCalendar.printCalendars() to see all your calendars and find out this id. 