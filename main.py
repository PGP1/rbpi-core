import arduinoconnect

'''
Calls Arduino Connect, and then push data to cloud, but publishing
'''


def main():
    # Begin subscribing
    # Begin publishing data
    arduino = arduinoconnect
    arduino.push_data()


if __name__ == '__main__':
    while True:
        main()
