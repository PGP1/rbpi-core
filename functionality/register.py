#!/usr/bin/python2
import json
import requests
import sqlite3
import uuid
import iddevice
import paho.mqtt.client as mqtt
import logging


def register():

    '''
    main methods
    - connect()
    - disconnect()
    - subscribe()
    - publish ()
    '''

    broker_address = "110.174.81.168"
    port = 1883
    topic = "register_device"
    ID = iddevice.getID()
    payload = {'id': ID}

    def on_publish(client, userdata, result):
        print("registered device \n")
        pass

    def on_disconnect(client, userdata, rc):
        logging.debug("disconnected, rc=", str(rc))
        client.loop_stop()
        print("client disconnected OK")
            
    # Create new instance
    client = mqtt.Client("awsiot-client-register")
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # set broker address of raspberry pis
    # connect to pi
    client.connect(broker_address, port)

    # publish to topic for AWS IoT to pickup
    client.publish(topic, json.dumps(payload))
    client.disconnect()


register()
