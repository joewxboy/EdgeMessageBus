FROM python:3-alpine

RUN python -m pip install --upgrade pip && \
    pip3 install schedule requests paho-mqtt

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

COPY docker-entrypoint.sh /usr/bin/
COPY *.py /usr/bin/
RUN chmod 755 /usr/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
CMD ["python", "/usr/bin/app.py"]