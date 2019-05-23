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
  -t mosqtt -f- ./ < Dockerfile.armhf
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

### Obtain a Weather Company API Key

Sign up for [IBM Cloud](https://cloud.ibm.com/login) and 
provision the [Weather Company Data service](https://cloud.ibm.com/catalog/services/weather-company-data). 
The Weather Company Data service uses the following [APIs](https://twcservice.mybluemix.net/rest-api/). 
You can reference [the documentation here](https://cloud.ibm.com/docs/services/Weather?topic=weather-insights_weather_overview).

### Get in the Right Directory

``` bash
cd ../Weather
```

### Define environment variables

Set your Weather API key `<YOUR_API_KEY>` and credentials `<YOUR_API_PASSWORD>` when running the application

``` bash
export WEATHER_API_KEY=<YOUR_API_KEY>
export WEATHER_API_URL=https://<YOUR_API_KEY>:<YOUR_API_PASSWORD>@twcservice.mybluemix.net/api/weather
export MQTT_USERNAME=[username here, ex. "mqtt"]
export MQTT_PASSWORD=[password here]
export MQTT_TOPIC=[topic here, ex. "test/json"]
export MQTT_BROKER="myqt"
```

### Build the Weather docker image and run it.

NOTE: The image will throw errors and die if an MQTT service is not available as configured.

``` bash
sudo docker build --build-arg MQTT_PASSWORD=${MQTT_PASSWORD} \
  --build-arg MQTT_USERNAME=${MQTT_USERNAME} \
  --build-arg MQTT_TOPIC=${MQTT_TOPIC} \
  --build-arg MQTT_BROKER=${MQTT_BROKER} \
  --build-arg WEATHER_API_KEY=${WEATHER_API_KEY} \
  --build-arg WEATHER_API_URL=${WEATHER_API_URL} \
  ./ -t wxapi
sudo docker run --rm -it --link myqt:myqt wxapi
```

### End of Installing the Weather API

TRY: Publish a location JSON Object to the MQTT Topic and watch the app respond with the weather forecast

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

## Install the WeatherHAT Display

### Get in the Right Directory

``` bash
cd ../Display
```

### Define environment variables

I'll assume you've already done this for a previous step.

### Build the WeatherHAT Display docker image and run it.

``` bash
sudo docker build --build-arg MQTT_PASSWORD=${MQTT_PASSWORD} \
  --build-arg MQTT_USERNAME=${MQTT_USERNAME} \
  --build-arg MQTT_TOPIC=${MQTT_TOPIC} \
  --build-arg MQTT_BROKER=${MQTT_BROKER} \
  --build-arg WEATHER_API_KEY=${WEATHER_API_KEY} \
  --build-arg WEATHER_API_URL=${WEATHER_API_URL} \
  ./ -t wxhat-pdm
sudo docker run --rm -it --device /dev/i2c-1 --privileged --link myqt:myqt wxhat-pdm
```

### End of Installing the WeatherHAT Display

TRY: Publish a location JSON Object to the MQTT Topic and watch the app respond

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
