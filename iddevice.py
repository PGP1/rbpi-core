#!/usr/bin/python2
import json
import requests
import sqlite3
import json
import uuid

def getID():
    conn = sqlite3.connect('rbpi-rmit-iot.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS info (id TEXT PRIMARY KEY)")

    c.execute("SELECT id FROM info")
    fetch = c.fetchone();
    FETCH_ID = fetch[0] if fetch != None else None;
    
    if(FETCH_ID == None):
        ID=str(uuid.uuid4()).replace('-','')
        print('initialise' + ID)
        c.execute("INSERT INTO info (id) VALUES (?)", [ID])
    else:
        ID = FETCH_ID

    conn.commit()
    conn.close()
    
    return ID
