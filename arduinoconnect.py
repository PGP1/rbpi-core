from time import sleep
# import serial
from pub import Publisher

#Established arduino connection
ser = ""
s = ""

def push_data():
        publisher = Publisher()
        publisher.publish('arduino')
        return 0