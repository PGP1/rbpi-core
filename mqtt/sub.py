
import paho.mqtt.client as mqtt
import json
import os
import utility.loadconfig as loadconfig
from dotenv import load_dotenv
env_path = './.env'
load_dotenv(dotenv_path=env_path)


class Subscriber:

    def __init__(self):
        self.command_topic = loadconfig.load_config()['topic']['fromawsiot/b1']
        self.response_topic = loadconfig.load_config()['topic']['statusresponse/b1']
        self.request_topic = loadconfig.load_config()['topic']['statusrequest/b1']
        self.BROKER_IP = os.getenv("BROKER_IP")
        self.BROKER_PORT = os.getenv("BROKER_PORT")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connection established, returned code=", rc)
            client.subscribe(self.command_topic)
            client.subscribe(self.request_topic)
        else:
            print("connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        print("topic: {} | payload: {} ".format(msg.topic, msg.payload))
        if msg.topic == "status_request/b1":
            payload = {"message": "On"}
            client.publish(self.response_topic, json.dumps(payload))

    def on_log(self, client, userdata, level, buf):
        print("log ", buf)

    def subscribe(self):
        broker_address = self.BROKER_IP
        # initialise MQTT Client
        client = mqtt.Client("pi-subscriber")

        # binds functions defined above, on connection, message and log
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_log = self.on_log

        # client.username_pw_set(user, password)
        client.connect(broker_address)
        client.loop_forever()
