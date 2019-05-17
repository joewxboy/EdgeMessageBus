# Mosquitto Service

## Details

This creates a Mosquitto service that listens on port 1883 by default.

## Security

The Dockerfile expects username and password to be specified in the environment variables `MQTT_USERNAME` and `MQTT_PASSWORD` prior to installation.

Those variables are passed into the Docker image `mosqtt` at build-time.

