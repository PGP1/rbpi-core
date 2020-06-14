"""
testing if mqtt protocol sends data properly
"""
import serial
import json
import paho.mqtt.client as mqtt
import time
import json
import pytest, os
import logging
import jsonschema

schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "broker-device": {
      "type": "string"
    },
    "payload": {
      "type": "object",
      "properties": {
        "time": {
          "type": "string"
        },
        "data": {
          "type": "object",
          "properties": {
            "temp": {
              "type": "integer"
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
        "time",
        "data"
      ]
    }
  },
  "required": [
    "broker-device",
    "payload"
  ]
}

# Established arduino connection
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
s = [0]
LOCALHOST = "localhost"

# Init client
client = mqtt.Client("Test")

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()

def test_sensorcollect():
    try:
        LOGGER.info('Serial Communicating')
        ser.flush()
        s[0] = ser.readline().decode().strip()
        payload = s[0]
        payloadJSON = json.loads(payload)
        print("[Serial] recieving data from Arduino | payload {}".format(payload))
        # Binds functions
        topic = "test_topic_sensor"
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(LOCALHOST) # Connect to broker
        client.loop_start() # Start loop

        client.subscribe(topic)
        client.publish(topic, payloadJSON)

        client.loop_stop() # Stop loop
        client.disconnect() # disconnect
    except Exception as e: 
        print('[Error] Decoding JSON has failed')
        print('[Error]', e)

# Functions to bind subscriber client.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to ", LOCALHOST)
    else:
        print("Bad connection")

def on_message(client, userdata, msg):
    """
    Decode the payload and store it.
    """
    payload = msg.payload
    m_decode = msg.payload.decode("utf-8", "ignore")
    print("Payload received from {} topic: {}" \
        .format(msg.topic, str(m_decode)))
    if msg.topic == 'test_topic_sensor':
        HELLO_RESP = str(m_decode)
        #assert payload == HELLO_RESP
        assert jsonschema.validate(payload, schema)
        

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected")
