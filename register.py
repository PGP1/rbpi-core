#!/usr/bin/python2
import json
import requests
import sqlite3
import json
import uuid
import time
import iddevice
import paho.mqtt.client as mqtt
import serial

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
    topic = "localgateway_to_awsiot"
    ID = iddevice.getID()

    def on_publish(client, userdata, result):
        print("data published \n")
        pass

    def on_disconnect(client, userdata, rc):
        logging.debug("disconnected, rc=",str(rc))
        client.loop_stop()
        print("client disconnected OK")
            
    # create new instance
    client = mqtt.Client("awsiot-client")
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect


    # set broker address of raspberry pis
    # connect to pi
    client.connect(broker_address,port)

    #Publish to topic 'localgateway_to_awsiot' for AWS IoT to pickup
    client.publish(topic, ID)
    client.disconnect()


register()
