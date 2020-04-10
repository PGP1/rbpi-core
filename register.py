#!/usr/bin/python2
import json
import requests
import sqlite3
import json
import uuid
import time

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

def register(id):
    ID = id
    print("Hello")
    # URL of the endpoint
    url = "https://yeotf6yzv3.execute-api.ap-southeast-2.amazonaws.com/default/RegisterDevice"
    
    # Payload, the id of the registered device
    payload = {'id': ID}
    
    headers = {
              'x-api-key': 'x2zEYge4bm4e40bYdQrlK3jc4h4c9OEh4muioDtf',
              'Content-Type': 'application/json'
              }
    
    while True:
        try:
            response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        except requests.ConnectionError as e:
            print("An exception occurred: ",  e)
            continue
        break

ID = getID()
register(ID)
