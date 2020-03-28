import paho.mqtt.client as mqtt
import time as time

mqtt_username = "linh"
mqtt_password = "chevron69" 
mqtt_topic = "test"
mqtt_port = "1883"
mqtt_broker_address= "52.64.12.23"

client = mqtt.Client("pp1")

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK returned code=", rc)
        client.subscribe(mqtt_topic)
    else:
        print("Bad connection returned code=", rc)

def on_message(client, userdata, msg):
    print("topic: {} | payload: {} ".format(msg.topic, msg.payload))

def on_log(client, userdata, level, buf):
    print("log: ", buf)

client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker_address)

client.loop_start()
client.subscribe("test")
print("subscribing to topic: test")
client.loop_forever()
