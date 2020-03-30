import paho.mqtt.client as mqtt
import time as time

user = "user"
password = "password"
#topic = "instruction/light"
topic = "test"
broker_address="110.174.81.168"
port = "1883"

print("creating new instance")
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


client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

print("connecting to broker")
#client.username_pw_set(user, password)
#client.connect(broker_address)

print("subscribing to topic"," instructions/light")
client.loop_start()
client.subscribe("test")
client.loop_forever()
