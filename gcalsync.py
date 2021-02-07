from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]


def main():
    tWService = build('calendar', 'v3', credentials=get_credentials("tw"))
    clientService = build('calendar', 'v3', credentials=get_credentials("client"))

    twEvent = getEvents(tWService)[0]
    event = createEvent(clientService, twEvent)
    listEvents(clientService)
    deleteEvent(clientService,event.get("id"))
    listEvents(clientService)

def deleteEvent(service, eventId):
    print("Deleting event with id: " + eventId)
    service.events().delete(calendarId='primary', eventId=eventId).execute()

def createEvent(service, sourceEvent):
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

    createdEvent = service.events().insert(calendarId='primary', body=eventBody).execute()
    print('Event created: ')
    print(createdEvent.get('htmlLink'))
    print(createdEvent)
    return createdEvent;

def listEvents(service):
    events = getEvents(service)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def getEvents(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def get_credentials(source):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    tokenPath = source + '.token.pickle'
    credentialsPath = source + '.credentials.json'

    if os.path.exists(tokenPath):
        with open(tokenPath, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsPath, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPath, 'wb') as token:
            pickle.dump(creds, token)

    return creds

if __name__ == '__main__':
    main()