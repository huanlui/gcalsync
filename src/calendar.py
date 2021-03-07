from __future__ import print_function

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from src.date_period import DatePeriod
import pickle
import os.path

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

class Calendar:
    def __init__(self, name):
        self.name = name
        self.service = self.__buildService(name)

    def getEvents(self, period: DatePeriod):
        events_result = self.service.events().list(calendarId='primary', timeMin=period.start,
                                            timeMax=period.end, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def deleteEvent(self, eventId):
        self.service.events().delete(calendarId='primary', eventId=eventId).execute()

    def createEventFrom(self,sourceEvent):
        eventBody = {
            'summary': sourceEvent.get('summary',''),
            'location': sourceEvent.get('location', ''),
            'description': sourceEvent.get('description', ''),
            'start': sourceEvent.get('start'),
            'end': sourceEvent.get('end'),
            'recurrence': sourceEvent.get('recurrence'),
            'attendees': [
            ],
            'reminders': sourceEvent.get('reminders'),
        }

        createdEvent = self.service.events().insert(calendarId='primary', body=eventBody).execute()

        return createdEvent

    def printEventsForPeriod(self, datePeriod: DatePeriod): 
        print('\n++++++++++++', self.name, 'calendar', '++++++++++++')
        self.printEvents(self.getEvents(datePeriod))
        print('++++++++++++++++++++++++++++++++++++++++++')
        
    
    def printEvents(self,events):
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    def __buildService(self,source):
        credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        tokenPath = source + '.token.pickle'
        credentialsPath = source + '.credentials.json'

        if os.path.exists(tokenPath):
            with open(tokenPath, 'rb') as token:
                credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentialsPath, SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(tokenPath, 'wb') as token:
                pickle.dump(credentials, token)

        return build('calendar', 'v3', credentials=credentials)

