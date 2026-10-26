#database.py
#scriot connecting to db
import sqlite3
from decimal import Decimal

def create_database():
    conn = sqlite3.connect('monitor.db')


    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS service_check (
                    check_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_url TEXT NOT NULL,
                    status TEXT NOT NULL,
                    http_status_code INTEGER,
                    response_time REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')

    conn.commit()
    conn.close()


def save_check(result):
    conn = sqlite3.connect('monitor.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO service_check 
        (service_url, status, http_status_code, response_time)
        VALUES (?, ?, ?, ?)
    ''', (
        result["url"],
        result["status"],
        result["http_status_code"],
        result["response_time"]

    ))
    conn.commit()
    conn.close()





#print("database connected") #TEMP CHECKING CODE


def get_all_checks(): #og testing code now function to retrieve all checks from the database
    conn = sqlite3.connect('monitor.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM service_check')
    rows = cursor.fetchall()

    conn.close()
    return rows



def get_total_checks():
    conn = sqlite3.connect('monitor.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM service_check')
    total_checks = cursor.fetchone()[0] # because thus sqlitemethod returns a list format like (value, )

    conn.close()
    return int(total_checks)

def get_status_count(status):

    conn = sqlite3.connect('monitor.db')
    cursor = conn.cursor()

    

    #cursor.execute(sql SELECT blah blah)
    #parametise status 
    cursor.execute(
        'SELECT COUNT(*) FROM service_check WHERE status = ?',
        (status,)

        )


    #fetch one row
    status_count = cursor.fetchone()[0] 


    #close conn
    #return 1st item
    conn.close()
    return int(status_count)


#avg response times
def get_avg_response_times():
    conn = sqlite3.connect('monitor.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT service_url, AVG(response_time)
        FROM service_check
        WHERE response_time IS NOT NULL
        GROUP BY service_url
    """)

    rows = cursor.fetchall()

    conn.close()
    #return Decimal(rows)
    return rows
    

def get_latest_check(service_url):
    conn = sqlite3.connect('monitor.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM service_check
        WHERE service_url = ?
        ORDER BY timestamp DESC, check_id DESC
        LIMIT 1
    """, (service_url,))

    row = cursor.fetchone()
    conn.close()
    return row



def get_services():
    conn = sqlite3.connect('monitor.db')
    cursor = conn.cursor()

    cursor.execute('SELECT DISTINCT service_url FROM service_check')
    services = cursor.fetchall()
    conn.close()
    return services

#TESTING CODE: checking db has saved results correctly:


#basically for each get_ function, conn, cursor, cursor.execute(sql query), fetch [0], close conn, return value.. 

#python sqlite notes
#conn is the connection to monitor.db from database.py
#cursor executes sql commands across the established connection

#sql functions: AVG(), COUNT(), MAX(), MIN(), SUM() 
#AVG() -> average of a column
#GROUP BY -> groups rows that have the same values into summary rows

#USE AVG + GROUPBY TO GET AVERAGE RESPONSE TIME PER SERVICE
