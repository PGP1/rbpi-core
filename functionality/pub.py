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

class Publisher:
    pub = ""
    broker_address = ""
    port = ""
    def __init__(self):
        self.broker_address = "110.174.81.168"
        self.port = 1883

    def on_publish(self, client, userdata, result):
        print("data published \n")
        pass

    def on_disconnect(self, client, userdata, rc):
        logging.debug("disconnected, rc=",str(rc))
        client.loop_stop()
        print("client disconnected OK")

    def publish(self, pub, payload):
        if pub == 'arduino':
            # setting topic to publish to
            topic = "localgateway_to_awsiot"

            # create new instance
            client = mqtt.Client("awsiot-client")
            client.on_publish = self.on_publish
            client.on_disconnect = self.on_disconnect

            # set broker address of raspberry pis
            # connect to pi
            client.connect(self.broker_address, self.port)

            #Publish to topic 'localgateway_to_awsiot' for AWS IoT to pickup
            client.publish(topic, json.dumps(payload))
            client.disconnect()
        elif pub == 'status':
            #Publish back to the AWSIoT to respond for request for online status
            client = mqtt.Client("awsiot-client-status")
            client.on_publish = self.on_publish
            client.on_disconnect = self.on_disconnect

            client.connect(self.broker_address, self.port)

            topic = "both_directions"
            payload = {"message": "On"}
            client.publish(topic, json.dumps(json.dumps(payload)))
            client.disconnect()
