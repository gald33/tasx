# coding=UTF-8

import MySQLdb
import random
import datetime
import iso8601


def taskDone(db, task_id):
    print ("updating task to completed")
    # update task
    # insert log


def feedback():
    # connect to server
    db = MySQLdb.connect("sql7.freemysqlhosting.net", "sql7114999", "Za2ZlsgmmM", "sql7114999")
    cursor = db.cursor()

    sql = "SELECT * FROM TASKS \
        WHERE start_time<'%s' AND alive=%s" % (datetime.datetime.now(), True)  # change start time to end time

    print (sql)

    try:
        print ("querying DB")
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        print ("reading")
        results = cursor.fetchall()
        for row in results:
            answer = raw_input("Did you complete task %s (%s, %s, %s)?" % (row[2], row[0], row[10], row[3]))
            if answer[0].lower() == "y":
                print ('Cool')
                taskDone(db, row[10])
            else:
                print ("don't sweat it, I'll schedule it for you")
                # call scheduler

    except:
        print ("query failed")
        # Rollback in case there is any error'''

    #  disconnect from server
    db.close()
