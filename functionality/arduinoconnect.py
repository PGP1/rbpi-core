# import serial
from mqtt.pub import Publisher
import json
import random
import time
from datetime import datetime
# Establish mock arduino data generation

def mock_temp():
    random.seed(datetime.now())
    return random.randint(0, 25)

def mock_humidity():
    random.seed(datetime.now())
    return random.randint(0, 75)

def mock_water():
    random.seed(datetime.now())
    return random.randint(330,350)

def mock_ph():
    random.seed(datetime.now())
    return random.uniform(5, 7)

def mock_light():
    random.seed(datetime.now())
    return random.randint(0, 255) 

def mock_data():
    mockArduinoPayload = {}
    data = {} 
    data["temp"] = mock_temp()
    data["humidity"] = mock_humidity()
    data["water"] = mock_water()
    data["ph"] = mock_ph()
    data["ldr"] = mock_light()

    mockArduinoPayload['data'] = data 
    return mockArduinoPayload

def push_data():
    try:
        time.sleep(1)
        payloadJSON = mock_data()
        print("[Mock] recieving data from Arduino | payload {}".format(payloadJSON))
        publisher = Publisher()
        publisher.publish('arduino', payloadJSON)
    except Exception as e: 
        print('[Error] Decoding JSON has failed')
        print('[Error]', e)
