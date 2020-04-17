from time import sleep
# import serial
from pub import Publisher

#Established arduino connection
ser = ""
s = {"message": "test"}

# ser = serial.Serial('/dev/ttyACM0', 9600)
# s = [0]

def push_data():
        publisher = Publisher()
        publisher.publish('arduino', s)