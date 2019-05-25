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

## Parts

* [WeatherHAT](https://shop.cyntech.co.uk/products/weatherhat) device
* [SDK](https://github.com/CyntechUK/WeatherHAT) and [Instructions](http://guides.cyntech.co.uk/weatherhat/getting-started/)
* RPi 3B+ with 32Gb MicroSD card
* Network connectivity
* Power
* [Docker](https://www.docker.com/products/docker-desktop)
* Code - TBD

## Configure I2C

From [this page](https://www.makeuseof.com/tag/enable-spi-i2c-raspberry-pi/).

Edit config.txt to uncomment i2c line, save, reboot.

``` bash
sudo vi /boot/config.txt
```

Uncomment line that contains `dtparam=i2c_arm=on` and save.

``` bash
sudo reboot
```

## Installation

To install, follow the directions in the [INSTALL.md](INSTALL.md) file.

## Credits

Display Dockerfile contents adapted from [Cyntech guide](http://guides.cyntech.co.uk/weatherhat/getting-started/#Connect_everything_up) instructions.

Weather API code adapted from the original work of [krook](https://github.com/krook) in the [`weather-api-python`](https://github.com/Call-for-Code/weather-api-python) repo, as well as substantial refactoring by [vabarbosa](https://github.com/vabarbosa) in his [fork](https://github.com/vabarbosa/weather-api-python).  It would not be possible without their contributions.
