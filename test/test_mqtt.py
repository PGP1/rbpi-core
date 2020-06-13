"""
testing if mqtt protocol sends data properly
"""

import paho.mqtt.client as mqtt
import time
import json

HELLO_TOPIC = "HELLO"
HELLO_MSG = "Hello World!"

LIST_TOPIC = "LIST"
LIST_MSG = [1, 2, 3]

LOCALHOST = "localhost"

# Init client
client = mqtt.Client("Test")

# Functions to bind subscriber client.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to ", LOCALHOST)
    else:
        print("Bad connection")

def on_message(client, userdata, msg):
    """
    Decode the payload and store it.
    """
    payload = msg.payload
    m_decode = msg.payload.decode("utf-8", "ignore")
    print("Payload received from {} topic: {}" \
        .format(msg.topic, str(m_decode)))
    if msg.topic == HELLO_TOPIC:
        HELLO_RESP = str(m_decode)
        assert HELLO_MSG == HELLO_RESP
    elif msg.topic == LIST_TOPIC:
        LIST_RESP = json.load(m_decode)
        assert LIST_MSG == LIST_RESP

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected")

def test_mqtt():
    # Binds functions
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(LOCALHOST) # Connect to broker
    client.loop_start() # Start loop

    client.subscribe(HELLO_TOPIC)
    client.publish(HELLO_TOPIC, HELLO_MSG)

    client.subscribe(LIST_TOPIC)
    client.publish(LIST_TOPIC, json.dumps(LIST_MSG))

    client.loop_stop() # Stop loop
    client.disconnect() # disconnect
