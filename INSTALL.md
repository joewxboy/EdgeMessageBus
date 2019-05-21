# Install Edge Message Bus

NOTE: These directions assume Raspbian on RPi 3 B+.

## Set up MQTT

Starting from your home directory or wherever you want to build this from (in my example, it is `/home/pi`):

### Clone EdgeMessageBus repo
``` bash
git clone https://github.com/joewxboy/EdgeMessageBus.git
cd EdgeMessageBus/Mosquitto
```

### Define MQTT Username and Password credentials in environment variables

``` bash
export MQTT_USERNAME=[username here, ex. "mqtt"]
export MQTT_PASSWORD=[password here]
```

### Build the Mosquitto docker image and run it.

This will create an image named `mosqtt`.

NOTE: Change `/home/pi` to your path prefix.

``` bash
sudo docker build --build-arg MQTT_PASSWORD=${MQTT_PASSWORD} \
  --build-arg MQTT_USERNAME=${MQTT_USERNAME} \
  -t mosqtt -f- /home/pi/EdgeMessageBus/Mosquitto/ < Dockerfile.armhf
sudo docker run --rm -it -p 1883:1883 mosqtt
```

### End of Installing MQTT
 
You have now created and exposed an MQTT server with the credentials you specified on the RPi at port 1883.

The server can be stopped by pressing Control-c in the terminal.

## Installing the Weather API



## Installing the WeatherHAT



## Installing the Node-RED Dashboard

