# import serial
from mqtt.pub import Publisher
import serial
import json
# Established arduino connection
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
s = [0]


def push_data():
    ser.flush()
    s[0] = ser.readline().decode().strip()
    payload = s[0].replace('"', "'")
    print(str(payload))
    try:
        publisher = Publisher()
        publisher.publish('arduino', payload)
    except Exception as e: 
        print('Decoding JSON has failed')
        print(e)
