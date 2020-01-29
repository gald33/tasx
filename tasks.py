# coding=UTF-8

import MySQLdb
import db_connection


############################################################################################
# NEW VERSION
############################################################################################

#####################
# middleman to db
#####################

def execute(sql, text):
    db = MySQLdb.connect(db_connection.host, db_connection.user, db_connection.password, db_connection.database)
    cursor = db.cursor()
    try:
        print (text)
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        print ("failed")
        # Rollback in case there is any error'''
        db.rollback()
    db.close()
    return cursor


#####################
# table
#####################

def drop_tasks_table():
    sql = "DROP TABLE tasks"
    text = "DROP TABLE tasks"
    execute(sql, text)


def create_tasks_table():
    sql = """CREATE TABLE `tasx`.`tasks` ( `task_id` INT(128) NOT NULL AUTO_INCREMENT , `event_id` VARCHAR(128)
     NOT NULL , `title` TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL , `start_time` TIMESTAMP NOT NULL ,
     `end_time` TIMESTAMP NOT NULL , PRIMARY KEY (`task_id`)) CHARACTER SET utf8 COLLATE utf8_unicode_ci
     ENGINE = InnoDB;"""
    text = "CREATE TABLE tasks"
    execute(sql, text)


def recreate_tasks_table():
    drop_tasks_table()
    create_tasks_table()


#####################
# task
#####################

class Task(object):
    def __init__(self, event_id, title, start_time, end_time):
        self.event_id = event_id
        # self.calendarId = calendar_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.alive = True
        self.completed = False
        self.movable = True
        self.times_postponed = 0
        self.color = "default"


def create_task_from_event(event):
    if event:
        task = Task(event['id'], event['summary'], event['start_time'], event['end_time'])
    else:
        print ("Creating task failed")
    return task


def insert_task(task):  # called by insert_task_list_to_db
    sql = """INSERT INTO TASKS (event_id, summary, start_time, end_time)
            VALUES ("%s","%s","%s","%s") ON DUPLICATE KEY
            UPDATE event_id="%s", summary="%s", start_time="%s", end_time="%s"
            """ % (task.event_id.encode('UTF-8'), task.summary.encode('UTF-8'),
                   task.start_time, task.end_time,
                   task.event_id.encode('UTF-8'), task.summary.encode('UTF-8'),
                   task.start_time, task.end_time)
    text = "Insert task"
    execute(sql, text)


#####################
# task list
#####################

def create_task_list_from_event_list(event_list):
    print ("Creating task list")
    task_list = []
    for event in event_list:
        task_list.append(create_task_from_event(event))
    return task_list


def insert_task_list_to_db(task_list):
    if task_list:
        for task in task_list:
            insert_task(task)
        return True
    else:
        print ("Can't insert task list, no\empty list")
        return False


def get_task_list_from_db():
    sql = "SELECT * FROM TASKS WHERE 1"
    text = "querying DB"
    results = execute(sql, text).fetchall()
    task_list = []
    for row in results:
        task_list.append(Task(row[1], row[2], row[3], row[4]))
    return task_list


#####################
# print
#####################

def print_task_list(task_list):
    if task_list:
        print ("Task list:")
        for task in task_list:
            print ("title:", task.title, "event_id:", task.event_id)
    else:
        print ("Can't print task list, no\empty list")


def print_all_tasks():
    print ('Printing all tasks')
    print_task_list(get_task_list_from_db())


############################################################################################
# OLD VERSION FUNCTIONS
############################################################################################

'''def create_task(event):
    if event:
        # currently we can create tasks only based on an event, because we need event id from gcal as unique in the DB
        #print ("Creating task from event")
        task = Task(event['id'], event['summary'], event['start_time'], event['end_time'])
    #elif row:
     #   print ("event_id: %s, summary: %s, start time: %s" % (row[0], row[2], row[3]))
      #  task = Task(row[0],row[2],row[3],row[4])
    else:
        print ("Creating task failed")
    return task
'''

'''def insert_task(db, task): # called by insert_task_list_to_db
    cursor = db.cursor()

    sql = """INSERT INTO TASKS (event_id, summary, start_time, end_time)
            VALUES ("%s","%s","%s","%s") ON DUPLICATE KEY

            UPDATE event_id="%s", summary="%s", start_time="%s", end_time="%s"
            """ % (task.event_id.encode('UTF-8'), task.summary.encode('UTF-8'),
                   task.start_time, task.end_time,
                   task.event_id.encode('UTF-8'), task.summary.encode('UTF-8'),
                   task.start_time, task.end_time)
    print (sql)
    ''''''
    , start_time, end_time
    , alive, completed,
            movable, times_postponed, color)

    , task.summary,

    ,
             task.alive, task.completed, task.movable, task.times_postponed, task.color

                                                        )
    ,'%s','%s','%s','%s','%s'
    , task.start_time, task.end_time

    alive='%s', completed='%s', movable='%s'
    ,'%s','%s','%s'

    ''''''
    try:
        print ("Inserting task to DB")
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()

    except:
        print ("Insertion failed")
        # Rollback in case there is any error
        db.rollback()
'''

'''def createTasksTable():
    db = MySQLdb.connect(db_connection.host, db_connection.user, db_connection.password, db_connection.database)
    cursor = db.cursor()
    sql = """CREATE TABLE `a7295373_tasx`.`tasks` (
        `task_id` INT NOT NULL AUTO_INCREMENT ,
        `event_id` VARCHAR( 128 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL ,
        `title` VARCHAR( 128 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL ,
        `start_time` DATETIME NOT NULL ,
        `end_time` DATETIME NOT NULL ,
        PRIMARY KEY ( `task_id` )
        ) ENGINE = MYISAM """
    try:
        print ("Creating tasks table")
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        print ("Insertion failed")
        # Rollback in case there is any error
        db.rollback()
    db.close()
'''


'''def recreateTasksTable():
    db = MySQLdb.connect(db_connection.host, db_connection.user, db_connection.password, db_connection.database)
    cursor = db.cursor()
    sql = """DROP TABLE `a7295373_tasx`.`tasks`"""
    try:
        print ("Creating tasks table")
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        print ("Insertion failed")
        # Rollback in case there is any error
        db.rollback()
    db.close()
'''

'''def get_task_list_from_db():
    # connect to DB server
    db = MySQLdb.connect("sql7.freemysqlhosting.net", "sql7114999", "Za2ZlsgmmM", "sql7114999")
    cursor = db.cursor()
    sql = "SELECT * FROM TASKS \
        WHERE 1"
    try:
        print ("querying DB")
        # Execute the SQL command
        cursor.execute(sql)
        results = cursor.fetchall()
        task_list =[]
        for row in results:
            task_list.append(Task(row[1],row[2],row[3],row[4]))
    except:
        print ("query failed")

    # disconnect from server
    db.close()
    return task_list'''