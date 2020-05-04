#!/usr/bin/python2
import json
import utility
import paho.mqtt.client as mqtt
import logging
import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path = './.env'
load_dotenv(dotenv_path=env_path)

BROKER_IP = os.getenv("BROKER_IP")
BROKER_PORT = os.getenv("BROKER_PORT")


def register():
    '''
    main methods
    - connect()
    - disconnect()
    - subscribe()
    - publish ()
    '''

    broker_address = BROKER_IP
    port = int(BROKER_PORT)
    print(port)
    topic = utility.loadconfig.load_config()['topic']['register']
    ID = utility.iddevice.get_id()
    payload = {'id': ID}

    def on_publish(client, userdata, result):
        print("registered device \n")
        print(payload)
        pass
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connection established, returned code=", rc)
        else:
            print("connection error, returned code=", rc)

    def on_log(client, userdata, level, buf):
        print("log ", buf)

    def on_disconnect(client, userdata, rc):
        logging.debug("disconnected, rc=", str(rc))
        client.loop_stop()

    # Create new instance
    client = mqtt.Client("awsiot-client")
    client.on_publish = on_publish
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # set broker address of raspberry pis
    # connect to pi
    client.connect(broker_address, port)

    # publish to topic for AWS IoT to pickup
    client.publish(topic, json.dumps(payload))
    client.disconnect()
