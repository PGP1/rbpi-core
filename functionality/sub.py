import paho.mqtt.client as mqtt
import time as time
import json
import os
from dotenv import load_dotenv

BROKER_IP = os.getenv("BROKER_IP")
BROKER_PORT = os.getenv("BROKER_PORT")

user = "user"
password = "password"
topic_1 = "awsiot_to_localgateway"
topic_2 = "both_directions"
broker_address = BROKER_IP
port = BROKER_PORT

# initialise MQTT Client
client = mqtt.Client("pi-subscriber")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connection established, returned code=", rc)
        client.subscribe(topic_1)
        client.subscribe(topic_2)
    else:
        print("connection error, returned code=", rc)


def on_message(client, userdata, msg):
    print("topic: {} | payload: {} ".format(msg.topic, msg.payload))
    if msg.topic == "both_directions":
        payload = {"message": "On"}
        client.publish(topic_2, json.dumps(payload))


def on_log(client, userdata, level, buf):
    print("log ", buf)


# binds functions defined above, on connection, message and log
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

# client.username_pw_set(user, password)
client.connect(broker_address)
client.loop_forever()

