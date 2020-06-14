import paho.mqtt.client as mqtt
import utility
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
topic = "unlink_device"


def on_publish(client, userdata, result):
    """
    Callback function, activates implementation once the client.publish is successful

    :param client: the client instance for this callback
    :type client: Client
    :param userdata: the private user data as set in Client() or
    user_data_set()
    :type userdata: any
    :param result: Data being published
    :type result: String
    """
    print("unliked device \n")
    pass


def on_disconnect(client, userdata, rc):
    """
    Callback function, activates implementation to run on disconnect

    :param client: the mqtt client
    :type client: Client
    :param userdata: the private user data as set in Client()
        or user_data_set()
    :type userdata: [type]
    :param rc: disconnection result
    :type rc: int
    """
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
