import sqlite3
import uuid

'''
This script performs the task of obtaining the ID of the device
via the local database
1) If the ID already exists, pulled from database
2) If not, generate the ID
'''


def get_id():
    conn = sqlite3.connect('../data/rbpi-rmit-iot.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS info (id TEXT PRIMARY KEY)")

    c.execute("SELECT id FROM info")
    fetch = c.fetchone()
    FETCH_ID = fetch[0] if fetch is not None else None

    if(FETCH_ID is None):
        ID = str(uuid.uuid4()).replace('-', '')
        print('initialise ' + ID)
        c.execute("INSERT INTO info (id) VALUES (?)", [ID])
    else:
        ID = FETCH_ID

    conn.commit()
    conn.close()
    return ID
