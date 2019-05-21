# Node-RED Dashboard Service

This will install a dashboard that allows you to see what is happening in the Edge Message Bus, as well as controlling it to an extent.

## Prerequisites

* Docker

## Installation

### Define MQTT credentials in environment variables

``` bash
export MQTT_USERNAME=[username here, ex. "mqtt"]
export MQTT_PASSWORD=[password here]
export MQTT_TOPIC=[topic here, ex. "test/json"]
export MQTT_BROKER=[broker URL here, ex. "http://127.0.0.1/"]
```

### Build the Node-RED Dashboard Docker image and run it.

``` bash
sudo docker build --build-arg MQTT_PASSWORD=${MQTT_PASSWORD} \
  --build-arg MQTT_USERNAME=${MQTT_USERNAME} \
  --build-arg MQTT_TOPIC=${MQTT_TOPIC} \
  --build-arg MQTT_BROKER=${MQTT_BROKER} \
   -t nred
sudo docker run --rm -it -p 1880:1880 --name nred
```