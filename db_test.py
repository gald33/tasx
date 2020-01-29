# coding=UTF-8

# connect to server
import MySQLdb
import random
import datetime
import iso8601

db = MySQLdb.connect("sql7.freemysqlhosting.net", "sql7114999", "Za2ZlsgmmM", "sql7114999")

cursor = db.cursor()

write = True
sql = """INSERT INTO TASKS (event_id, start_time)
            VALUES ('%s','%s')""" % (random.randint(1,1000000),
                                     (datetime.datetime.now()
                                     +datetime.timedelta(hours=1)))

print (sql)

if write:
    try:
        print ("querying DB")
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        print ("writing")
        db.commit()

    except:
        print ("query failed")
        # Rollback in case there is any error'''

sql = "SELECT * FROM TASKS \
    WHERE 1"

print (sql)

try:
    print ("querying DB")
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    print ("reading")
    results = cursor.fetchall()
    for row in results:
        print ("event_id: %s, summary: %s, start time: %s" % (row[0], row[2], row[3]))

except:
    print ("query failed")
    # Rollback in case there is any error'''

#  disconnect from server
db.close()
