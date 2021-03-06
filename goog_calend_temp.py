import logging
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

logging.basicConfig(filename='run.log', level=logging.DEBUG)


def add_events(schedule_events, token='token.json'):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token):
        creds = Credentials.from_authorized_user_file(token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token, 'w') as token0:
            token0.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        # Prints the start and name of the next 10 events
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

        for sEvent in schedule_events:
            try:
                Sevent = service.events().insert(calendarId='primary',
                                                 body=sEvent, sendUpdates='all').execute()
                print("Added event to calendar : "+str(Sevent.get('htmlLink')))
            except Exception:
                print("Couldn't add event : " + str(sEvent))
                logging.exception(Exception)

    except HttpError as error:
        print('An HTTP error occurred: %s' % error)
