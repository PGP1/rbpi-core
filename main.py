import functionality.arduinoconnect as arduino
from mqtt.sub import Subscriber
'''
Calls Arduino Connect, and then push data to cloud, but publishing
'''


def main():
    # Begin subscribing
    subscriber = Subscriber()
    subscriber.subscribe()

    # Begin publishing data
    arduino = arduino
    arduino.push_data()


if __name__ == '__main__':
    while True:
        main()
