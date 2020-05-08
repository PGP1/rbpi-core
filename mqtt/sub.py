
import paho.mqtt.client as mqtt
import json
import os
import utility.loadconfig as loadconfig
import utility.statusdevice as statusdevice
import utility.iddevice as iddevice
import utility.resetdevice as resetdevice
import serial
import datetime
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
        payloadJSON = json.loads(msg.payload)
        
        if msg.topic == "status_request/b1":
            payload = {}
            payload['broker-id'] = iddevice.get_id()
            payload['type'] = 'resources'
            payload['time'] = datetime.datetime.now().isoformat()
            payload['status'] = 'On'
            payload['uptime'] = statusdevice.get_uptime()
            payload['cpu-percent'] = statusdevice.get_cpu_percent()
            payload['ram'] = statusdevice.get_ram_usage()
            client.publish(self.response_topic, json.dumps(payload))
            print(json.dumps(payload))
        elif payloadJSON['controller']['type'] == 'raspberrypi':
            resetdevice.reset_device()
        elif payloadJSON['controller']['type'] == 'arduino':
            print("[Mock] sent commands to arduino | payload {} of type {}".format(msg.payload, type(msg.payload)))

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
