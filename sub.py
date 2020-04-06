import paho.mqtt.client as mqtt
import time as time

user = "user"
password = "password"
topic = "awsiot_to_localgateway"
broker_address="110.174.81.168"
port = "1883"

#initialise MQTT Client
client = mqtt.Client("pi-subscriber")

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connection established, returned code=",rc)
        client.subscribe(topic)
    else:
        print("connection error, returned code=",rc)

def on_message(client, userdata, msg):
    print("topic: {} | payload: {} ".format(msg.topic, msg.payload))

def on_log(client, userdata, level, buf):
    print("log ", buf)

# Binds functions defined above, on connection, message and log
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

#client.username_pw_set(user, password)
client.connect(broker_address)

client.loop_forever()
