# coding=UTF-8
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

import MySQLdb
import random
import datetime
import iso8601
import scheduler

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def create_event(summary,scheduled_time, length_in_minutes):
    event = {
        'summary': summary,
        # 'location': '800 Howard St., San Francisco, CA 94103',
        # 'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': scheduled_time.isoformat(),
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': (scheduled_time + datetime.timedelta(minutes=length_in_minutes)).isoformat(),
            'timeZone': 'Asia/Jerusalem',
        },
    }
    return event


def get_basic_event_list(): # and service
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # get events from gcal
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting upcoming events from google calendar')
    event_list = []
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            eventsResult = service.events().list(
                calendarId=calendar_list_entry['id'], timeMin=now,
                timeMax=(iso8601.parse_date(now) + datetime.timedelta(days=5)).isoformat(), singleEvents=True,
                orderBy='startTime').execute()
            event_list += eventsResult.get('items', [])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    return event_list


def add_times_to_event_list(event_list):  # includes start time and end time as datetime objects
    if event_list:
        for event in event_list:
            event['start_time'] = iso8601.parse_date(event['start'].get('dateTime', event['start'].get('date')))
            event['end_time'] = iso8601.parse_date(event['end'].get('dateTime', event['end'].get('date')))
    else:
        print ("can't add times to event list, no\empty list")
        return False
    return event_list


def get_event_list_with_times():  # includes start time and end time as datetime objects
    return add_times_to_event_list(get_basic_event_list())


def sort_event_list(event_list):
    # sort all events by date
    print("\nSorting...\n")
    event_list.sort(key=lambda item: item['start_time'])


def add_free_time_to_event_list(event_list):
    # Add free time attribute - time between the last and current event
    sort_event_list(event_list)
    for index, event in enumerate(event_list):
        if not index:
            event['freeTime'] = event['start_time'] - iso8601.parse_date(datetime.datetime.utcnow().isoformat())
        else:
            event['freeTime'] = event['start_time'] - event_list[index - 1]['end_time']
    return event_list


def get_event_list_with_free_time():
    return add_free_time_to_event_list(get_event_list_with_times())


def print_event_list_names(event_list):   # also calculates free time
    if event_list:
        for index, event in enumerate(event_list):
            print("event", event['summary'])
        return True
    else:
        print("Can't print event list, no\empty list")
        return False


def print_event_list_with_times(event_list):   # also calculates free time
    if event_list:
        for index, event in enumerate(event_list):
            if not index:
                event['freeTime'] = event['start_time'] - iso8601.parse_date(datetime.datetime.utcnow().isoformat())
                print("\nFree time between events:", event['freeTime'])
            else:
                event['freeTime'] = event['start_time'] - event_list[index - 1]['end_time']
                print("\nFree time between events:", event['freeTime'])
            print("event", event['summary'], "\nFrom", event['start_time'], "\nUntil", event['end_time'],
                                     "\nDuration is",
                                     event['end_time'] - event['start_time'], "\n")

        return True
    else:
        print("Can't print event list, no\empty list")
        return False


def print_all_events():
    print ("Printing all events")
    print_event_list_with_times(get_event_list_with_free_time())


def insert_event_to_gcal(title, length_in_minutes, calendar_id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = create_event(title, scheduler.find_time(length_in_minutes), length_in_minutes)
    event = service.events().insert(
        calendarId=calendar_id, body=event).execute()
    print('Event created: %s' '%s' % (event.get('htmlLink'), event.get('eventId')))
    return event


#########################################################################################
# OLD VERSION
#########################################################################################
'''def insert_event_to_gcal(event, calendar_id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    scheduled_time = scheduler.find_time(60)
    summary = "TEST23:19"
    length_in_minutes = 60
    event = {
        'summary': summary,
        # 'location': '800 Howard St., San Francisco, CA 94103',
        # 'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': scheduled_time.isoformat(),
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': (scheduled_time + datetime.timedelta(minutes=length_in_minutes)).isoformat(),
            'timeZone': 'Asia/Jerusalem',
        },
    }

    event = service.events().insert(
        calendarId=calendar_id, body=event).execute()
    print('Event created: %s' '%s' % (event.get('htmlLink'), event.get('eventId')))
    return event'''