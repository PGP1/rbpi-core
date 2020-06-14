# import serial
from mqtt.pub import Publisher
import serial
import json
import jsonschema
import utility
# Established arduino connection
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
s = [0]

schema = utility.loadconfig.load_config()['schema-arduino']


def push_data():
    try:
        ser.flush()
        s[0] = ser.readline().decode().strip()
        payload = s[0]
        payloadJSON = json.loads(payload)
        print("[Serial] recieving data from Arduino | payload {}".format(payload))
        try:
            jsonschema.validate(payloadJSON, schema)
            publisher = Publisher()
            publisher.publish('arduino', payloadJSON['data'])
        except Exception as e:
            print("[Error] Not valid json format")
            print('[Error]', e)
    except Exception as e:
        print('[Error] Decoding JSON has failed')
        print('[Error]', e)
