#!/usr/bin/python2
import json
import requests
import sqlite3
import json
import uuid
import time
import iddevice

def register():
    ID = iddevice.getID()
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

register()
