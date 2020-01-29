# coding=UTF-8


#not used
#from __future__ import unicode_literals

#from __future__ import print_function

#from sched import scheduler

#import httplib2
#import os

#from apiclient import discovery
#import oauth2client
#from oauth2client import client
from oauth2client import tools

import datetime
import pytz
import iso8601
import random

#####################
# modules
#####################

import feedback
import scheduler
import tasks
import events

# Check cmd line arguments
mode = 'add'
title = 'test 10:35'


def main():
    while True:
        if mode == 'tasklist':
            tasks.print_all_tasks()
            break
        elif mode == 'eventlist':
            events.print_all_events()
            break
        elif mode == 'add':
            scheduler.add_event_and_task_to_db(title)
            break
        elif mode == 'feedback':
            feedback.feedback()
            break
        elif mode == 'build_db':
            tasks.createTasksTable()
            break
        elif mode == 'rebuild_db':
            tasks.recreate_tasks_table()
            break
        else:
            # WASNT IMPLEMENTED YET
            print ('What would you like to do?')
            break

if __name__ == '__main__':
    main()
