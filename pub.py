import paho.mqtt.client as mqtt
import serial

#arduino setup
ser = serial.Serial('/dev/ttyACM0',9600)
s = [0]

'''
main methods
- connect()
- disconnect()
- subscribe()
- publish ()
'''
broker_address = "110.174.81.168"
port = 1883
topic = "localgateway_to_awsiot"

def on_publish(client, userdata, result):
    print("data published \n")
    pass

def on_disconnect(client, userdata, rc):
    logging.debug("disconnected, rc=",str(rc))
    client.loop_stop()
    print("client disconnected OK")
        
# create new instance
client = mqtt.Client("client1")
client.on_publish = on_publish
client.on_disconnect = on_disconnect
# client.publish("sensor/water_level","LOW")

# set broker address of raspberry pis
# connect to pi
client.connect(broker_address,port)
# publish a message


read_serial=ser.readline()
s[0] = str(int (ser.readline(),16))

client.publish(topic, s[0])
#client.publish(topic, "{\"key\": \"helloFromLocalGateway\"}")
client.disconnect()
