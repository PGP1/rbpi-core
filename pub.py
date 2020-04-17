import paho.mqtt.client as mqtt
import serial
import json

'''
main methods
- connect()
- disconnect()
- subscribe()
- publish ()
'''

broker_address = "110.174.81.168"
port = 1883
pub =" " 

def __init__(self, publisher):
    self.pub = publisher

def on_publish(client, userdata, result):
    print("data published \n")
    pass

def on_disconnect(client, userdata, rc):
    logging.debug("disconnected, rc=",str(rc))
    client.loop_stop()
    print("client disconnected OK")

def publish(pub):
    if pub == 'arduino':
        # arduino setup
        ser = serial.Serial('/dev/ttyACM0', 9600)
        s = [0]
        topic = "localgateway_to_awsiot"

	# create new instance
        client = mqtt.Client("awsiot-client")
        client.on_publish = on_publish
        client.on_disconnect = on_disconnect

        # set broker address of raspberry pis
        # connect to pi
        client.connect(broker_address,port)

        # publish a message
        read_serial=ser.readline()
        s[0] = ser.readline()

        #Publish to topic 'localgateway_to_awsiot' for AWS IoT to pickup
        client.publish(topic, s[0])
        client.disconnect()
    elif pub == 'status':
        client = mqtt.Client("awsiot-client-status")
        client.on_publish = on_publish
        client.on_disconnect = on_disconnect

        client.connect(broker_address, port)

        topic = "both_directions"
        payload = {"message": "On"}
        client.publish(topic, json.dumps(payload))
        client.connect(broker_address, port)

publish(pub)