# import serial
from mqtt.pub import Publisher
import serial
import json
import jsonschema
# Established arduino connection
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
s = [0]

schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "broker-device": "c0cb03a49a754a17b07b85c4d4f19039",
            "payload": {
                "time": "2020-06-14T06:17:07.086056",
                "data": {
                    "temp": 16.5,
                    "humidity": 77,
                    "water": 907,
                    "ph": 6.687825,
                    "ldr": 0
                }
            }
        }
    ],
    "required": [
        "broker-device",
        "payload"
    ],
    "additionalProperties": true,
    "properties": {
        "broker-device": {
            "$id": "#/properties/broker-device",
            "type": "string",
            "title": "The broker-device schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "c0cb03a49a754a17b07b85c4d4f19039"
            ]
        },
        "payload": {
            "$id": "#/properties/payload",
            "type": "object",
            "title": "The payload schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "time": "2020-06-14T06:17:07.086056",
                    "data": {
                        "temp": 16.5,
                        "humidity": 77,
                        "water": 907,
                        "ph": 6.687825,
                        "ldr": 0
                    }
                }
            ],
            "required": [
                "time",
                "data"
            ],
            "additionalProperties": true,
            "properties": {
                "time": {
                    "$id": "#/properties/payload/properties/time",
                    "type": "string",
                    "title": "The time schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": "",
                    "examples": [
                        "2020-06-14T06:17:07.086056"
                    ]
                },
                "data": {
                    "$id": "#/properties/payload/properties/data",
                    "type": "object",
                    "title": "The data schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": {},
                    "examples": [
                        {
                            "temp": 16.5,
                            "humidity": 77,
                            "water": 907,
                            "ph": 6.687825,
                            "ldr": 0
                        }
                    ],
                    "required": [
                        "temp",
                        "humidity",
                        "water",
                        "ph",
                        "ldr"
                    ],
                    "additionalProperties": true,
                    "properties": {
                        "temp": {
                            "$id": "#/properties/payload/properties/data/properties/temp",
                            "type": "number",
                            "title": "The temp schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": 0.0,
                            "examples": [
                                16.5
                            ]
                        },
                        "humidity": {
                            "$id": "#/properties/payload/properties/data/properties/humidity",
                            "type": "integer",
                            "title": "The humidity schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": 0,
                            "examples": [
                                77
                            ]
                        },
                        "water": {
                            "$id": "#/properties/payload/properties/data/properties/water",
                            "type": "integer",
                            "title": "The water schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": 0,
                            "examples": [
                                907
                            ]
                        },
                        "ph": {
                            "$id": "#/properties/payload/properties/data/properties/ph",
                            "type": "number",
                            "title": "The ph schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": 0.0,
                            "examples": [
                                6.687825
                            ]
                        },
                        "ldr": {
                            "$id": "#/properties/payload/properties/data/properties/ldr",
                            "type": "integer",
                            "title": "The ldr schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": 0,
                            "examples": [
                                0
                            ]
                        }
                    }
                }
            }
        }
    }
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
