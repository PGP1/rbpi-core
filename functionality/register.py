"""
module that contains code that will register the raspberry pi device
"""
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
    """
    A class that contains register logic
    """
    broker_address = BROKER_IP
    port = int(BROKER_PORT)
    print(port)
    topic = utility.loadconfig.load_config()['topic']['register']
    ID = utility.iddevice.get_id()
    payload = {'id': ID}

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
        print("registered device \n")
        print(result)
        pass

    def on_connect(client, userdata, flags, rc):
        """
        Callback function, activates implementation to run on connect

        :param client: the mqtt client
        :type client: Client
        :param userdata: the private user data as set in Client()
            or user_data_set()
        :type userdata: [type]
        :param rc: disconnection result
        :type rc: int
        """
        if rc == 0:
            print("connection established, returned code=", rc)
        else:
            print("connection error, returned code=", rc)

    def on_log(client, userdata, level, buf):
        """
        Callback function, activates implementation to run on log.

        :param userdata: the private user data as set in Client() or
        user_data_set()
        :type userdata: any
        :param level: severity of the message
        :type level: MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING,
        MQTT_LOG_ERR, MQTT_LOG_DEBUG
        :param buf: message buffer
        :type buf: bytes
        """
        print("log ", buf)

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
