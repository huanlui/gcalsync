from __future__ import print_function
from src.date_period import DatePeriod
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

COPIED_EVENT_LEADING_TEXT = '[CLIENT MEETING]'

NUM_RETRIES = 10

def as_datetime(time_object):
    iso_value = time_object['dateTime'] if 'dateTime' in time_object else time_object['date']
    return datetime.fromisoformat(iso_value)

def start_and_end_equal(event1, event2):
    try:
        return as_datetime(event1['start']) == as_datetime(event2['start']) and as_datetime(event1['end']) == as_datetime(event2['end'])
    except KeyError as e:
        raise Exception("Events lack (start,end).dateTime: %s" % {"event1": event1, "event2": event2}) from e

class Calendar:
    def __init__(self, calendarId, googleService):
        self.calendarId = calendarId
        self.googleService = googleService

    def copyAllEventsFrom(self, otherCalendar, period: DatePeriod, copySensibleData, colorId, skipMatching):
        events = otherCalendar.getEvents(period)
        existing_events = self.getEvents(period)
        self.removeCopiedEvents(existing_events)

        for event in events:
            if not skipMatching or not any(start_and_end_equal(event, e) for e in existing_events):
                self.createEventFrom(event, copySensibleData, colorId)

    def getEvents(self, period: DatePeriod):
        events = []
        page_token = None
        while True:
            events_result = self.googleService.events().list(calendarId=self.calendarId, timeMin=period.start,
                                                             timeMax=period.end, singleEvents=True,
                                                             orderBy='startTime', pageToken=page_token).execute(num_retries=NUM_RETRIES)
            events.extend(events_result['items'])
            page_token = events_result.get('nextPageToken')
            if not page_token:
                break

        return events

    def removeCopiedEvents(self, events):
        eventsToRemove = list(
            filter(lambda event: COPIED_EVENT_LEADING_TEXT in event.get('summary', ''), events))
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
