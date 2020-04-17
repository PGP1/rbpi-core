import arduinoconnect

def main():
    arduino = arduinoconnect
    arduino.push_data()

if __name__=='__main__':
    while True:
        main()

