import pyodbc
import uuid
import calendar
import time
from datetime import datetime
from threading import Thread

report_ids = {}
def get_report(report_id):
    if report_ids[report_id]=="GENERATING":
        return "Running"
    return "Complete"

def trigger_report():
    report_id = uuid.uuid1()
    report_ids[report_id]= "GENERATING"
    t1 = Thread(target=generate_report(report_id))
    t1.start()
    return report_id

def generate_report(report_id):
    store_ids=get_store_ids()
    uptime_last_hour=[]
    uptime_last_day=[]
    uptime_last_week=[]
    downtime_last_hour=[]
    downtime_last_day=[]
    downtime_last_week=[]
    for store_id in store_ids:
        uptime_last_hour.append(get_uptime_last_hour(store_id))

def get_uptime_last_hour(store_id):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=DESKTOP-4KMT3JP\SQLEXPRESS;'
                          'Database=DatasetLoop;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute("select timestamp from activity where store_id=? and status=?",store_id,"active")
    rows = cursor.fetchall()
    timestamps = []
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    date_time_now = datetime.fromtimestamp(time_stamp)
    time_stamp -= 3600
    date_time_before = datetime.fromtimestamp(time_stamp)
    start_day=date_time_before.weekday()
    date_time_start = get_start_time(start_day,store_id,date_time_before)
    for row in rows:
        date_time_1 = datetime. strptime(row.timestamp[:-4], '%Y-%m-%d %H:%M:%S.%f')
        if date_time_1>=date_time_before:
            timestamps.append(date_time_1)

def get_start_time(start_day,store_id,date_time_before):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=DESKTOP-4KMT3JP\SQLEXPRESS;'
                          'Database=DatasetLoop;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute("select * from menuhours")
    rows = cursor.fetchall()
    if len(rows) == 0:
        return date_time_before
    cursor.execute("select * from timezones where store_id=?",store_id)
    rows = cursor.fetchall()
    time_zone = "America/Chicago"
    if len(rows) != 0:
        time_zone = rows[0].timezone
    cursor.execute("select start_time, end_time from menuhours where store_id=? and day=?",store_id,start_day)
    rows = cursor.fetchall()
    start_time = datetime.strptime(rows[0].timestamp, '%Y-%m-%d %H:%M:%S.%f')








def get_store_ids():
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=DESKTOP-4KMT3JP\SQLEXPRESS;'
                          'Database=DatasetLoop;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute("select distinct store_id as sid from activity")
    rows = cursor.fetchall()
    store_ids= []
    for row in rows:
        store_ids.append(row.sid)
    return store_ids