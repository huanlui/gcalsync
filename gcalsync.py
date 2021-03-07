from src.date_period import DatePeriod
from src.calendar import Calendar

def main():
    twCalendar = Calendar("tw")
    clientCalendar = Calendar("client")

    twCalendar.printEventsForPeriod(DatePeriod.days(1))
    clientCalendar.printEventsForPeriod(DatePeriod.days(1))

    twEvent = twCalendar.getEvents(DatePeriod.days(1))[0]
    event = clientCalendar.createEventFrom(twEvent)
    clientCalendar.printEventsForPeriod(DatePeriod.days(1))

    clientCalendar.deleteEvent(event.get("id"))
    clientCalendar.printEventsForPeriod(DatePeriod.days(1))

if __name__ == '__main__':
    main()