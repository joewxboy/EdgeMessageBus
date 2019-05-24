# Edge Message Bus

## TL;DR

This is a multi-architecture approach to defining and using a specific format of JSON messages to publish information in a decoupled, many-to-many topology.  The goal is to send specific information without knowing in advance who will consume it, or for what purpose it will be used.

It is comprised of: 

* an MQTT service, powered by Mosquitto
* a Weather service, powered by The Weather Company
* an LED display service, using the WeatherHAT by Cyntech
* a dashboard service for visualization and control, using Node-RED

![](diagram.png)

## Architecture

The message bus is powered by Mosquitto.

The JSON schema is my own, loosely based on previous work done for _The Weather Company, an IBM Business_.

The architectures supported include ARMv6 and AMD64, but may be easily ported to others.

