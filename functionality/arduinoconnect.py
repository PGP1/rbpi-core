# import serial
from mqtt.pub import Publisher
import serial
import json
# Established arduino connection
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
s = [0]


def push_data():
    try:
        ser.flush()
        s[0] = ser.readline().decode().strip()
        payload = s[0]
        payloadJSON = json.loads(payload)
        publisher = Publisher()
        publisher.publish('arduino', payloadJSON['data'])
    except Exception as e: 
        print('[Error] Decoding JSON has failed')
        print('[Error]', e)
