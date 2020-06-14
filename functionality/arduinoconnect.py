# import serial
from mqtt.pub import Publisher
import serial
import json
import jsonschema
# Established arduino connection
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
s = [0]

schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "device": {
      "type": "string"
    },
    "data": {
      "type": "object",
      "properties": {
        "temp": {
          "type": "number"
        },
        "humidity": {
          "type": "integer"
        },
        "water": {
          "type": "integer"
        },
        "ph": {
          "type": "number"
        },
        "ldr": {
          "type": "integer"
        }
      },
      "required": [
        "temp",
        "humidity",
        "water",
        "ph",
        "ldr"
      ]
    }
  },
  "required": [
    "device",
    "data"
  ]
}

def push_data():
    try:
        ser.flush()
        s[0] = ser.readline().decode().strip()
        payload = s[0]
        payloadJSON = json.loads(payload)
        print("[Serial] recieving data from Arduino | payload {}".format(payload))
        if jsonschema.validate(payloadJSON, schema):
            publisher = Publisher()
            publisher.publish('arduino', payloadJSON['data'])
        else:
            print("[Error] Not valid json format")
    except Exception as e: 
        print('[Error] Decoding JSON has failed')
        print('[Error]', e)
