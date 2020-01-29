# coding=UTF-8

import MySQLdb
import random
import datetime
import iso8601
import tasks
import events


def find_time(length_in_minutes):
    # finding free time
    event_list = events.get_event_list_with_free_time()
    for event in event_list:
        if event['freeTime'] > datetime.timedelta(minutes=length_in_minutes):
            scheduled_time = event['start_time'] - datetime.timedelta(minutes=length_in_minutes)
            print(scheduled_time, "is a good fit for this event")
            break
        else:
            print("NOT GOOD")
    return scheduled_time


def create_event(summary, scheduled_time, length_in_minutes):
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


def add_event_and_task_to_db(title):
    event = events.insert_event_to_gcal(title, 60, 'ef23mcq3sc293gm19aagt7dcs@group.calendar.google.com')
    event_list = [event]
    task_list = tasks.create_task_list_from_event_list(event_list)
    tasks.insert_task_list_to_db(task_list)