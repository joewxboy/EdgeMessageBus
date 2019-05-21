# Install Edge Message Bus

NOTE: These directions assume Raspbian on RPi 3 B+.

## Install MQTT

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
sudo docker run --rm -it -p 1883:1883 --name myqt mosqtt
```

### End of Installing MQTT
 
You have now created and exposed an MQTT server with the credentials you specified on the RPi at port 1883.

The server can be stopped by pressing Control-c in the terminal.

TRY: Connect to your MQTT Server with a client (I like MQTTLens), subscribe to your MQTT_TOPIC, and publish a small JSON object to your MQTT_TOPIC and watch it show up in your subscription.

``` json
{
    "type":"location",
    "loctype":"geocode",
    "data":{
        "lat":"34.02",
        "lon":"-84.62"
    },
    "child":[]
}
```

## Install the Weather API



## Install the WeatherHAT Display



## Install the Node-RED Dashboard

Assuming you are still in the `Display` directory, change over to the `Node-RED` folder:

``` bash
cd ../Node-RED
```

### Define required environment variables

``` bash
export MQTT_USERNAME=[username here, ex. "mqtt"]
export MQTT_PASSWORD=[password here]
export MQTT_TOPIC=[topic here, ex. "test/json"]
export MQTT_BROKER="myqt"
```

NOTE: The TOPIC and BROKER variables are new, and weren't defined earlier.

### Build the Node-RED Dashboard Docker image and run it.

``` bash
sudo docker build --build-arg MQTT_PASSWORD=${MQTT_PASSWORD} \
  --build-arg MQTT_USERNAME=${MQTT_USERNAME} \
  --build-arg MQTT_TOPIC=${MQTT_TOPIC} \
  --build-arg MQTT_BROKER=${MQTT_BROKER} \
  -t nred -f- ./ < Dockerfile.armhf
sudo docker run --rm -it -p 1880:1880 --link myqt:myqt nred
```

NOTE: The above refers to a Dockerfile for the `armhf` architecture, like the Raspberry Pi. 
If you're using an x86_64 machine, use the `Dockerfile.amd64` file instead. 

### End of Installing the Node-RED Dashboard

TRY: Connect to the Node-RED Dashboard web UI in your browser at: 
http://[machine IP address]:1880/ui/#/0

If you have the Mosquitto, Weather, and Display services running, 
then you should be able to click a button for a location and see the 
corresponding weather for that location load into the center of the dashboard, 
and the buttons representing the Display light up for five seconds for the 
relevant indicators for that location's weather.