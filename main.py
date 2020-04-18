import arduinoconnect
import time 

'''
Calls Arduino Connect, and then push data to cloud, but publishing
'''

def main():
    arduino = arduinoconnect
    arduino.push_data()

if __name__=='__main__':
    while True:
        # time.sleep(1000)
        main()

