# RBPI-Core (Plantly)
Tests, configs and setup instructions for our Raspberry Pi - Arduino IoT Smart Garden: Plantly.

Data capturing using Arduino Microcontroller

- Each raspberry pi will have an unique id.
- On first run:
	- Hash token is saved
	- New folder data is created
- Data files are saved as format: ID-day-month-year-hour-min-sec.csv

## 1 Prerequisite

- Python3 3.7.3+
- Mosquitto 1.5.7 MQTT Protocol Library
- Python Library for Paho-MQTT
- Raspberry Pi Device (we are using RPI 3)

requirements.txt
- paho-mqtt
- psutil
- python-dotenv
- pyserial

### 1.1 Dependencies: 

#### Set up Virtual Environment
Install virtualenv, and create a virtual environment to install dependencies
``` bash
pip3 install virtualenv

virtualenv venv
```

Activate the venv (virtual env called venv)
``` bash
source venv/bin/activate
```

Install dependencies
``` bash
pip3 install -r requirements.txt
```

Running on RaspianOS (Install MQTT)
``` bash
sudo apt install mosquitto
```


### 1.2 Setting up the Device for Videostreaming, pushing sensor data & listening for dashboard commands

Ensure that your credentials are assigned to environment variables
- Access Key
- Secret Key
- Default Region
* NEVER HARDCODE YOUR CREDENTIALS, utilise $ENVIRONMENTVARIABLE

Make sure its executable, if its not then run
```bash
chmod +x <scriptname>.sh
```

#### Setting up MQTT on the Raspberry Pi

- Refer to **4.1 How to run bridge MQTT Broker to AWS IoT** to link the device to IoT Core and establish PUB/SUB communication with Cloud Architecture

- Remember to set a .env file

``` bash 
touch .env

vim .env
```

Copy 

``` bash
BROKER_IP=localhost
BROKER_PORT=1883
```
#### Setting up Garden Sensor collection

Ensure that the Arduino is connected via serial cable, refer to **Arduino repo** for instructions to deploy controller_main.ino sketch


## 2 Deployment
### 2.1 Deploying MQTT PUB/SUB Communication 
> Pre-req: Arduino must be connected via serial cable, and the .ino file (sensor code) deployed

To push data collected from sensor
``` bash
python3 main.py
```
> Open up another terminal tab WHY: This method is for DEBUG to see the logs 

To run subscriber to receieve commands from Dashboard
``` bash
python3 startup.py
```

### 2.2 Deploying up your Videostream

> Open up another terminal tab

*check your environment variables are set for your credentials
``` bash
./docker.sh
```

Now the device is ready to receive commands from the dashboard, to push collected data from sensors & videostreaming is running.

## 3 Testing





## 4 Additional Setup 

### 4.1 How to run bridge MQTT Broker to AWS IoT

In the terminal of your device

``` bash
 mosquitto_pub -h localhost -p 1883 -q 1 -d -t localgateway_to_awsiot  -i clientid1 -m "{\"key\": \"helloFromLocalGateway\"}"
```

*Note: This will publish the localhost, being the IP Address of the PI, on port 1883, sending a QoS of 1, on the topic localgateway_to_awsiot with the identity of clientid1, sending a JSON Format message


## How to configure another device (either EC2 Instance, microcontroller, Pi or your own local machine)

Make sure you install Mosquitto onto the Pi

``` bash
sudo apt-get install mosquitto && sudo apt-get instal mosquitto-clients
```

#### Configure the CLI with your region, enter in region/credentials

``` bash
aws configure
```

#### Create an IAM policy for the bridge
```
aws iot create-policy --policy-name bridge --policy-document '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Action": "iot:*","Resource": "*"}]}'
```


#### Place yourself in Mosquitto directory and create certificates and keys, note the certificate ARN
``` bash
cd /etc/mosquitto/certs/
```
``` bash
sudo aws iot create-keys-and-certificate --set-as-active --certificate-pem-outfile cert.crt --private-key-outfile private.key --public-key-outfile public.key --region <region>
```

#### List the certificate and copy the ARN 
``` bash
aws iot list-certificates
```

#### Attach the policy to your certificate
``` bash
aws iot attach-principal-policy --policy-name bridge --principal <arn>
```

#### Add read permissions to private key and client cert
``` bash
sudo chmod 644 private.key
sudo chmod 644 cert.crt
sudo chmod 644 private.key
```

#### Create your rootCA.pem  
``` bash
sudo touch rootCA.pem
```

1. Copy all of the highlighted text below, including `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`
2. Paste the copied contents into a plain text editor such as Notepad or Vi. Do not use a rich-text editor, such as Word.
3. Save the file with a .txt, .cer, or .pem extension.

```
 -----BEGIN CERTIFICATE----- 
 MIIE0zCCA7ugAwIBAgIQGNrRniZ96LtKIVjNzGs7SjANBgkqhkiG9w0BAQUFADCB yjELMAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQL ExZWZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTowOAYDVQQLEzEoYykgMjAwNiBWZXJp U2lnbiwgSW5jLiAtIEZvciBhdXRob3JpemVkIHVzZSBvbmx5MUUwQwYDVQQDEzxW ZXJpU2lnbiBDbGFzcyAzIFB1YmxpYyBQcmltYXJ5IENlcnRpZmljYXRpb24gQXV0 aG9yaXR5IC0gRzUwHhcNMDYxMTA4MDAwMDAwWhcNMzYwNzE2MjM1OTU5WjCByjEL MAkGA1UEBhMCVVMxFzAVBgNVBAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQLExZW ZXJpU2lnbiBUcnVzdCBOZXR3b3JrMTowOAYDVQQLEzEoYykgMjAwNiBWZXJpU2ln biwgSW5jLiAtIEZvciBhdXRob3JpemVkIHVzZSBvbmx5MUUwQwYDVQQDEzxWZXJp U2lnbiBDbGFzcyAzIFB1YmxpYyBQcmltYXJ5IENlcnRpZmljYXRpb24gQXV0aG9y aXR5IC0gRzUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCvJAgIKXo1 nmAMqudLO07cfLw8RRy7K+D+KQL5VwijZIUVJ/XxrcgxiV0i6CqqpkKzj/i5Vbex t0uz/o9+B1fs70PbZmIVYc9gDaTY3vjgw2IIPVQT60nKWVSFJuUrjxuf6/WhkcIz SdhDY2pSS9KP6HBRTdGJaXvHcPaz3BJ023tdS1bTlr8Vd6Gw9KIl8q8ckmcY5fQG BO+QueQA5N06tRn/Arr0PO7gi+s3i+z016zy9vA9r911kTMZHRxAy3QkGSGT2RT+ rCpSx4/VBEnkjWNHiDxpg8v+R70rfk/Fla4OndTRQ8Bnc+MUCH7lP59zuDMKz10/ NIeWiu5T6CUVAgMBAAGjgbIwga8wDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8E BAMCAQYwbQYIKwYBBQUHAQwEYTBfoV2gWzBZMFcwVRYJaW1hZ2UvZ2lmMCEwHzAH BgUrDgMCGgQUj+XTGoasjY5rw8+AatRIGCx7GS4wJRYjaHR0cDovL2xvZ28udmVy aXNpZ24uY29tL3ZzbG9nby5naWYwHQYDVR0OBBYEFH/TZafC3ey78DAJ80M5+gKv MzEzMA0GCSqGSIb3DQEBBQUAA4IBAQCTJEowX2LP2BqYLz3q3JktvXf2pXkiOOzE p6B4Eq1iDkVwZMXnl2YtmAl+X6/WzChl8gGqCBpH3vn5fJJaCGkgDdk+bW48DW7Y 5gaRQBi5+MHt39tBquCWIMnNZBU4gcmU7qKEKQsTb47bDN0lAtukixlE0kF6BWlK WE9gyn6CagsCqiUXObXbf+eEZSqVir2G3l6BFoMtEMze/aiCKm0oHw0LxOXnGiYZ 4fQRbxC1lfznQgUy286dUV4otp6F01vvpX1FQHKOtw5rDgb7MzVIcbidJ4vEZV8N hnacRHr2lVz2XTIIM6RUthg/aFzyQkqFOFSDX9HoLPKsEdao7WNq 
 -----END CERTIFICATE-----
```

Save as rootCA.pem in the same directory as above certificated. You can also create your own CA, please refer to online documentation to IoT Core Credentials. 

#### Create the configuration file

``` bash
#Create the configuration file
sudo nano /etc/mosquitto/conf.d/bridge.conf
```

To find your AWS endpoint, enter aws iot describe-endpoint

> ```
> #Copy paste the following in the nano editor:
> # =================================================================
> # Bridges to AWS IOT
> # =================================================================
> 
> # AWS IoT endpoint, use AWS CLI 'aws iot describe-endpoint'
> connection awsiot
> address XXXXXXXXXX.iot.<region>.amazonaws.com:8883
> 
> # Specifying which topics are bridged
> topic awsiot_to_localgateway in 1
> topic localgateway_to_awsiot out 1
> topic both_directions both 1
> 
> # Setting protocol version explicitly
> bridge_protocol_version mqttv311
> bridge_insecure false
> 
> # Bridge connection name and MQTT client Id,
> # enabling the connection automatically when the broker starts.
> cleansession true
> clientid bridgeawsiot
> start_type automatic
> notifications false
> log_type all
> 
> # =================================================================
> # Certificate based SSL/TLS support
> # -----------------------------------------------------------------
> #Path to the rootCA
> bridge_cafile /etc/mosquitto/certs/rootCA.pem
> 
> # Path to the PEM encoded client certificate
> bridge_certfile /etc/mosquitto/certs/cert.crt
> 
> # Path to the PEM encoded client private key
> bridge_keyfile /etc/mosquitto/certs/private.key
> ```


#### Start the mosquitto broker with this configuration


Starts Mosquitto in the background
``` bash
sudo mosquitto -c /etc/mosquitto/conf.d/bridge.conf –d
```

Starts Mosquitto with logs (use for DEBUG)
``` bash
sudo mosquitto -c /etc/mosquitto/conf.d/bridge.conf
```

Enable Mosquitto to run at startup automatically
``` bash
sudo chkconfig --level 345 scriptname on
```

Test by publishing to the topic, going into AWS IoT > Test and subcribing to 'localgate_to_awsiot'
``` bash
mosquitto_pub -h localhost -p 1883 -q 1 -d -t localgateway_to_awsiot  -i clientid1 -m "{\"key\": \"helloFromLocalGateway\"}"
```
