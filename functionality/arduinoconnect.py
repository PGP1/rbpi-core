import serial
from mqtt.pub import Publisher

# Established arduino connection
# ser = serial.Serial('/dev/ttyACM0', 9600)
# s = [0]


def push_data():
    publisher = Publisher()
    publisher.publish('arduino', 'test')
