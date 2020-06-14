"""
module that contains logic for subscribe.
"""
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

ser = serial.Serial('/dev/ttyACM0', baudrate=115200, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO, bytesize=serial.EIGHTBITS)


class Subscriber:
    """
    A class that contains subscriber logic.
    """

    def __init__(self):
        """
        initialises the topic routes which it will listen to, 
        ip address, port, username.
        """
        self.command_topic = loadconfig.load_config()['topic']['fromawsiot/b1']
        self.response_topic = loadconfig.load_config()[
            'topic']['statusresponse/b1']
        self.request_topic = loadconfig.load_config()[
            'topic']['statusrequest/b1']
        self.BROKER_IP = os.getenv("BROKER_IP")
        self.BROKER_PORT = os.getenv("BROKER_PORT")

    def on_connect(self, client, userdata, flags, rc):
        """
        subscribe to the topics that were initialised.

        :param client: the client instance for this callback
        :type client: Client
        :param userdata: the private user data as
        set in Client() or user_data_set()
        :type userdata: any
        :param flags: response flags sent by the broker
        :type flags: dict
        :param rc: result of connection
        :type rc: integer
        """
        if rc == 0:
            print("connection established, returned code=", rc)
            client.subscribe(self.command_topic)
            client.subscribe(self.request_topic)
        else:
            print("connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        """
        prints out the topic and payload, prints to console different messages
        depending on topic. Also handles saving pictures if topic is facial
        recognition.

        :param client: the client instance for this callback
        :type client: Client
        :param userdata: the private user data as set in Client()
        or user_data_set()
        :type userdata: any
        :param msg: an instance of MQTTMessage. This is a class with members
        topic, payload, qos, retain.
        :type msg: MQTTMessage
        """
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
            ser.write(msg.payload)
            print("[Serial] sent commands to arduino | payload {} of type {}".format(
                msg.payload, type(msg.payload)))

    def on_log(self, client, userdata, level, buf):
        """
        function to run for logging.

        :param client: the client instance for this callback
        :type client: Client
        :param userdata: the private user data as set in Client() or
        user_data_set()
        :type userdata: any
        :param level: severity of the message
        :type level: MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING,
        MQTT_LOG_ERR, MQTT_LOG_DEBUG
        :param buf: message buffer
        :type buf: bytes
        """
        print("log ", buf)

    def subscribe(self):
        """
        initialises mqtt client. binds on connect, message and log functions to
        the client. connects to the address and starts loop.
        """
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
