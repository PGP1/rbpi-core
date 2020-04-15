import paho.mqtt.client as mqtt
import serial
import register
import json
import iddevice

broker_address = "110.174.81.168"
port = 1883
topic = "unlink-device"

def on_publish(client, userdata, result):
    print("unliked device \n")
    pass

def on_disconnect(client, userdata, rc):
    logging.debug("disconnected, rc=",str(rc))
    client.loop_stop()
    print("client disconnected OK")
                                
# create new instance
client = mqtt.Client("awsiot-client-unlink")
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# connect to pi
client.connect(broker_address,port)

#getID
id = {'id': iddevice.getID()}
#Publish to topic 'unlink' for AWS IoT to pickup
client.publish(topic, json.dumps(id))
client.disconnect()