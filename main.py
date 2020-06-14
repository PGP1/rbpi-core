'''
Calls Arduino Connect, pushes sensordata by retrieving sensor data from Arduino
'''
import functionality.arduinoconnect as arduino


def main():
    # Begin publishing data
    arduino.push_data()


if __name__ == '__main__':
    while True:
        main()
