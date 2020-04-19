import paho.mqtt.client as mqtt
import json
import logging
import os
import utility.loadconfig as loadconfig
import utility.iddevice as iddevice

BROKER_IP = os.getenv("BROKER_IP")
BROKER_PORT = os.getenv("BROKER_PORT")

'''
methods
- connect()
- disconnect()
- subscribe()
- publish ()
'''


class Publisher:
    pub = ""
    broker_address = ""
    port = ""

    def __init__(self):
        self.broker_address = BROKER_IP
        self.port = BROKER_PORT

    def on_publish(self, client, userdata, result):
        print("data published \n")
        pass

    def on_disconnect(self, client, userdata, rc):
        logging.debug("disconnected, rc=", str(rc))
        client.loop_stop()
        print("client disconnected OK")

    def publish(self, pub, payload):
        if pub == 'arduino':
            # setting topic to publish to
            topic = loadconfig.load_config().topic['toawsiot/b1']
            id = iddevice.get_id()
            payload = {'device': {'pi-id' : id}, 'message': payload}

            # create new instance
            client = mqtt.Client("awsiot-client")
            client.on_publish = self.on_publish
            client.on_disconnect = self.on_disconnect

            # set broker address of raspberry pis
            # connect to pi
            client.connect(self.broker_address, self.port)

            # Publish to topic 'localgateway_to_awsiot/b1' for AWS IoT to pickup
            client.publish(topic, json.dumps(payload))
            client.disconnect()
        elif pub == 'status':
            # Publish back to the AWSIoT to respond for request for online
            # status
            client = mqtt.Client("awsiot-client-status")
            client.on_publish = self.on_publish
            client.on_disconnect = self.on_disconnect

            client.connect(self.broker_address, self.port)

            topic = loadconfig.load_config().topic['toawsiot/b1']
            id = iddevice.get_id()
            payload = {'device': {'pi-id' : id}, 'message': 'on'}
            client.publish(topic, json.dumps(json.dumps(payload)))
            client.disconnect()
