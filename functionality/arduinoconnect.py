# import serial
from mqtt.pub import Publisher

# Established arduino connection
# ser = serial.Serial('/dev/ttyACM0', 9600)
# s = [0]


def push_data():
    testpayload={'device': 'arduino-id',
    'time': '20-18-04T11:24:36Z',
    'data': {
        'temp': '30',
        'humidity': '30',
        'water': '330',
        'ph': '7',
        'ldr': '485',
    }}
    publisher = Publisher()
    publisher.publish('arduino', testpayload)
