import datetime
#import pytz
from zoneinfo import ZoneInfo
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

"""
NOTE: you may have to run the following code in your terminal before running the code:
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main(task_name, description, creation_date, due_date):
  """Shows basic usage of the Google Calendar API.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)

      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    

    '''Example Task to Add to Calendar -- Format for App Usage
    event = {
        'summary': 'CSC 450 Project Task 3', #pull task name
        'location': '', #is this required? we dont have anything set up in the UI
        'description': 'Working on that project', #pull task description (can be null)
        'start': { #date created
            'dateTime': '2024-11-20T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': { #pull task due date
            'dateTime': '2024-11-21T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [ #is this required? we dont have anything set up in the UI
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [ # will need current session user's Email
            {'email': 'parrish298@gmail.com'},
            {'email': 'enoellemoore@gmail.com'},
        ],
        'reminders': { #is this required? we dont have anything set up in the UI
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }'''

    new_event = create_event(task_name, description, now, due_date)

    insert_event(service, new_event)
    # Inserts Event
    #event = service.events().insert(calendarId='primary', body=event).execute()
    
    #print('Event created: %s' % (event.get('htmlLink')))





  except HttpError as error:
    print(f"An error occurred: {error}")

def create_event(task_name, description, creation_date, due_date):
  print('now: ' + creation_date)
  print('due date: ' + due_date)
  event = {
        'summary': task_name, #pull task name
        'description': description, #pull task description (can be null)
        'start': { #date created
            'dateTime': creation_date,
            'timeZone': 'America/New_York',
        },
        'end': { #pull task due date
            'dateTime': format_due_date(due_date),
            'timeZone': 'America/New_York',
        }
  }
  return event

def insert_event(service, event):
  event = service.events().insert(calendarId='primary', body=event).execute()
  print('Event created: %s' % (event.get('htmlLink')))
  return

def format_due_date(date):
  original_date = date
  parsed_date = datetime.datetime.strptime(original_date, "%Y-%m-%dT%H:%M")
  formatted_date = parsed_date.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
  return formatted_date
