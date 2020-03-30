# RBPI-Core

Basic Data capturing using Sense Hat.

- Each raspberry pi will have an unique id.
- On first run:
	- Hash token is saved in local sqlite3 under rbpi-rmit-iot.db
	- New folder data is created
- Data files are saved as format: ID-day-month-year-hour-min-sec.csv

Todo:
- [ ] Modify to work with other sensors.
- [ ] Arduino database serialise

## How to run bridge MQTT Broker to AWS IoT

In the terminal of the pi

> mosquitto_pub -h localhost -p 1883 -q 1 -d -t localgateway_to_awsiot  -i clientid1 -m "{\"key\": \"helloFromLocalGateway\"}"

*Note: This will publish the localhost, being the IP Address of the PI, on port 1883, sending a QoS of 1, on the topic localgateway_to_awsiot with the identity of clientid1, sending a JSON Format message