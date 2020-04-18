import paho.mqtt.client as mqtt
import iddevice
import logging
import os
import json

BROKER_IP = os.getenv("BROKER_IP")
BROKER_PORT = os.getenv("BROKER_PORT")

'''
Unlink Device, by publishing ID to Cloud,
and it will find in the dynamoDB database
and update by removing it
'''

broker_address = BROKER_IP
port = BROKER_PORT
topic = "unlink-device"


def on_publish(client, userdata, result):
    print("unliked device \n")
    pass


def on_disconnect(client, userdata, rc):
    logging.debug("disconnected, rc=", str(rc))
    client.loop_stop()
    print("client disconnected OK")


# create new instance
client = mqtt.Client("awsiot-client-unlink")
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# connect to pi
client.connect(broker_address, port)

# getID
id = {'id': iddevice.getID()}
# Publish to topic 'unlink' for AWS IoT to pickup
client.publish(topic, json.dumps(id))
client.disconnect()
