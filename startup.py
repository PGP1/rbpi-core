import mqtt.sub as subscriber
import functionality.register as register 
def start_up():
    # On start up of the device, the device will subscribe to topics
    sub = subscriber.Subscriber()
    sub.subscribe()

    # Will register itself, it hasn't already
    register.register()

start_up()
