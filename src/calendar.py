from __future__ import print_function
from src.date_period import DatePeriod

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

COPIED_EVENT_LEADING_TEXT = '[CLIENT MEETING]'

NUM_RETRIES = 10

class Calendar:
    def __init__(self, calendarId, googleService):
        self.calendarId = calendarId
        self.googleService = googleService

    def copyAllEventsFrom(self, otherCalendar, period: DatePeriod, copySensibleData, colorId):
        self.removeCopiedEvents(period)
        for event in otherCalendar.getEvents(period):
            self.createEventFrom(event, copySensibleData, colorId)

    def getEvents(self, period: DatePeriod):
        events_result = self.googleService.events().list(calendarId=self.calendarId, timeMin=period.start,
                                                         timeMax=period.end, singleEvents=True,
                                                         orderBy='startTime').execute(num_retries=NUM_RETRIES)
        events = events_result.get('items', [])
        return events

    def removeCopiedEvents(self, period: DatePeriod):
        eventsToRemove = list(
            filter(lambda event: COPIED_EVENT_LEADING_TEXT in event.get('summary', ''), self.getEvents(period)))
        for event in eventsToRemove:
            self.deleteEvent(event.get("id"))

    def deleteEvent(self, eventId):
        self.googleService.events().delete(calendarId=self.calendarId, eventId=eventId).execute(num_retries=NUM_RETRIES)

    def createEventFrom(self, sourceEvent, copySensibleData, colorId):
        eventBody = {
            'summary': (COPIED_EVENT_LEADING_TEXT + ' ' + sourceEvent.get('summary',
                                                                          '')) if copySensibleData else COPIED_EVENT_LEADING_TEXT,
            'location': sourceEvent.get('location', '') if copySensibleData else '',
            'description': sourceEvent.get('description', '') if copySensibleData else '',
            'start': sourceEvent.get('start'),
            'end': sourceEvent.get('end'),
            'recurrence': sourceEvent.get('recurrence'),
            'attendees': [
            ],
            'reminders': sourceEvent.get('reminders'),
        }
        if colorId:
            eventBody['colorId'] = colorId

        createdEvent = self.googleService.events().insert(calendarId=self.calendarId, body=eventBody).execute(num_retries=NUM_RETRIES)

        return createdEvent

    def printEventsForPeriod(self, datePeriod: DatePeriod):
        print('\n++++++++++++', self.calendarId, 'calendar', '++++++++++++')
        self.printEvents(self.getEvents(datePeriod))
        print('++++++++++++++++++++++++++++++++++++++++++')

    def printEvents(self, events):
        if not events:
            print('No upcoming events found.')
        for event in events:
            # start = event['start'].get('dateTime', event['start'].get('date'))
            # print(start, event['summary'])
            print(event)
