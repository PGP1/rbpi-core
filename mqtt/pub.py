import paho.mqtt.client as mqtt
import json
import logging
import os
import utility
import datetime
from dotenv import load_dotenv
env_path = './.env'
load_dotenv(dotenv_path=env_path)

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
    def __init__(self):
        self.broker_address = str(BROKER_IP)
        self.port = int(BROKER_PORT)

    def on_publish(self, client, userdata, result):
        print("[Publish] data published \n")
        pass

    def on_disconnect(self, client, userdata, rc):
        logging.debug("disconnected, rc=", str(rc))
        client.loop_stop()
        print("[Publish] client disconnected OK")

    def publish(self, pub, arduinopayload):
        print("[Publish] Sending to: ", self.broker_address)
        print("[Publish] on: ", self.port)
        if pub == 'arduino':
            # setting topic to publish to
            topic = utility.loadconfig.load_config()['topic']['toawsiot/b1']
            brokerID= utility.iddevice.get_id()
            now_time = datetime.datetime.now().now().isoformat()
            
            print(arduinopayload)
            publishJSON = {}
            payload = {}
            
            data = arduinopayload["data"]
            payload['data'] = data
            publishJSON['payload'] = payload
            
            publishJSON['broker-device'] = brokerID
            payload['time'] = now_time
            # create new instance
            client = mqtt.Client("awsiot-client")
            client.on_publish = self.on_publish
            client.on_disconnect = self.on_disconnect
            
            # set broker address of raspberry pis
            # connect to pi
            client.connect(self.broker_address, self.port)
            
            print(publishJSON)
            #Publish to topic 'localgateway_to_awsiot/b1' for AWS IoT to pickup
            client.publish(topic, json.dumps(publishJSON))
            client.disconnect()
        elif pub == 'status':
            # Publish back to the AWSIoT to respond for request for online
            # status
            client = mqtt.Client("awsiot-client-status")
            client.on_publish = self.on_publish
            client.on_disconnect = self.on_disconnect

            client.connect(self.broker_address, self.port)

            topic = loadconfig.load_config()['topic']['toawsiot/b1']
            id = iddevice.get_id()
            payload = {'broker-device': id, 'payload': 'On'}
            client.publish(topic, json.dumps(payload))
            client.disconnect()
