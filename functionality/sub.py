import paho.mqtt.client as mqtt
import json
import os
import utility


class Subscriber:

    def __init__(self):
        self.topic_1 = utility.loadconfig.load_config().topic['toawsiot/b1']
        self.topic_2 = utility.loadconfig.load_config().topic['status_request/b1']
        self.BROKER_IP = os.getenv("BROKER_IP")
        self.BROKER_PORT = os.getenv("BROKER_PORT")
        
    def on_connect(self, client, userdata, flags, rc):
            if rc == 0:
                print("connection established, returned code=", rc)
                client.subscribe(self.topic_1)
                client.subscribe(self.topic_2)
            else:
                print("connection error, returned code=", rc)


    def on_message(self, client, userdata, msg):
        print("topic: {} | payload: {} ".format(msg.topic, msg.payload))
        if msg.topic == "both_directions":
            payload = {"message": "On"}
            client.publish(self.topic_2, json.dumps(payload))


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
