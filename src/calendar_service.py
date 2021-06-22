from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
from .calendar import Calendar

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

COPIED_EVENT_LEADING_TEXT = '[CLIENT MEETING]'


class CalendarService:
    def __init__(self, accountName):
        self.googleService = self.__buildGoogleService(accountName)

    def printCalendars(self):
        page_token = None
        while True:
            calendar_list = self.googleService.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(calendar_list_entry['summary'])
                print(calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    def getCalendar(self, calendarId):
        return Calendar(calendarId, self.googleService)

    def __buildGoogleService(self, source):
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
