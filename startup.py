'''
Initiates a subscriber to listen for dashboard commands
'''
import mqtt.sub as subscriber
import functionality.register as register


def start_up():
    
    # Will register itself, it hasn't already
    register.register()

    # On start up of the device, the device will subscribe to topics
    sub = subscriber.Subscriber()
    sub.subscribe()
    
start_up()
