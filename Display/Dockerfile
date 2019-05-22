FROM raspbian/stretch

# Install required dependencies
RUN apt-get -y update && apt-get -y install sudo wget curl jq build-essential python-dev git scons swig python-smbus python-pip python3-gpiozero python-gpiozero python-pkg-resources python3-pkg-resources python-rpi.gpio python3-rpi.gpio && pip install paho-mqtt

ARG MQTT_USERNAME
ARG MQTT_PASSWORD
ARG MQTT_TOPIC
ARG MQTT_BROKER
ARG WEATHER_API_KEY
ARG WEATHER_API_URL

ENV MQTT_PASSWORD=$MQTT_PASSWORD
ENV MQTT_USERNAME=$MQTT_USERNAME
ENV MQTT_TOPIC=$MQTT_TOPIC
ENV MQTT_BROKER=$MQTT_BROKER
ENV WEATHER_API_KEY=$WEATHER_API_KEY
ENV WEATHER_API_URL=$WEATHER_API_URL

# Download the code
RUN git clone https://github.com/jgarff/rpi_ws281x.git
RUN git clone https://github.com/CyntechUK/WeatherHAT.git

COPY *.py /WeatherHAT/

WORKDIR /rpi_ws281x
RUN scons

WORKDIR /rpi_ws281x/python
RUN python setup.py install

WORKDIR /WeatherHAT


COPY docker-entrypoint.sh /usr/bin/
RUN chmod 755 /usr/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
CMD ["python", "/WeatherHAT/app.py"]