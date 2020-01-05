from __future__ import print_function
import pickle
import csv
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# header
DATE = "DATE"
SUMMARY = "SUMMARY"
DESCRIPTION = "DESCRIPTION"
LOCATION = "LOCATION"

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    with open("schedule.csv", "r", encoding="shift-jis") as f:
        reader = csv.DictReader(f)

        for data in reader:
            date = data[DATE].split("/")
            summary = data[SUMMARY]
            description = data[DESCRIPTION]
            location = data[LOCATION]

            year = date[0]
            month = date[1]
            day = date[2]

            print("LOG : Success!", year, month, day, summary)
            event = {
            'summary': summary,
            'location': location,
            "kind": "calendar#event",
            'description': description,
            'start': {
                'date': '{}-{}-{}'.format(year, month, day),
                'timeZone': 'Japan',
            },
            'end': {
                'date': '{}-{}-{}'.format(year, month, day),
                'timeZone': 'Japan',
            },
            }

            event = service.events().insert(calendarId='your calender ID', body=event).execute()

if __name__ == '__main__':
    main()

