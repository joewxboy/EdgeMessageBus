FROM python:3-alpine

RUN apk add git gcc python3-dev musl-dev && python -m pip install --upgrade pip && \
    pip3 install schedule requests paho-mqtt scons smbus2 gpiozero

# FROM raspbian/stretch

# Install required dependencies
# RUN apt-get -y update && apt-get -y build-essential python-dev git scons swig python-smbus python-pip python3-gpiozero python-gpiozero python-pkg-resources python3-pkg-resources python-rpi.gpio python3-rpi.gpio && pip install paho-mqtt

ARG MQTT_USERNAME
ARG MQTT_PASSWORD
ARG MQTT_TOPIC
ARG MQTT_BROKER

ENV MQTT_PASSWORD=$MQTT_PASSWORD
ENV MQTT_USERNAME=$MQTT_USERNAME
ENV MQTT_TOPIC=$MQTT_TOPIC
ENV MQTT_BROKER=$MQTT_BROKER

# Download the code
RUN git clone https://github.com/jgarff/rpi_ws281x.git
RUN git clone https://github.com/CyntechUK/WeatherHAT.git

COPY *.py /WeatherHAT/

WORKDIR /rpi_ws281x
RUN sed -i 's/0755/0o755/g' SConscript && scons

WORKDIR /rpi_ws281x/python
RUN python setup.py install

WORKDIR /WeatherHAT

COPY docker-entrypoint.sh /usr/bin/
RUN chmod 755 /usr/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
CMD ["python", "/WeatherHAT/app.py"]