from src.date_period import DatePeriod
from src.calendar import Calendar

def main():
    twCalendar = Calendar("tw", "primary")
    
    clientCalendarId = "" ## Put here the ID of your client calendar visible from your TW account
    ## use  twCalendar.printCalendars() to see all your calendars and find out this id. 
    clientCalendar = Calendar("tw", clientCalendarId )

    twCalendar.copyAllEventsFrom(clientCalendar, DatePeriod.weeks(1))

if __name__ == '__main__':
    main()