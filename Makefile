sudo docker build --build-arg MQTT_PASSWORD=${MQTT_PASSWORD} --build-arg MQTT_USERNAME=${MQTT_USERNAME} -t mosqtt -f- /Users/josephpearson/dev/EdgeMessageBus/Mosquitto/ < Dockerfile.armhf

sudo docker build --build-arg MQTT_PASSWORD=${MQTT_PASSWORD} --build-arg MQTT_USERNAME=${MQTT_USERNAME} -t mosqtt -f- /Users/josephpearson/dev/EdgeMessageBus/Mosquitto/ < Dockerfile.amd64 

sudo docker run --rm -it -p 1883:1883 mosqtt

sudo docker build -t loc2mqtt -f- /Users/josephpearson/dev/EdgeMessageBus/Location/ < Dockerfile.amd64 

sudo docker run --rm -it -link loc2mqtt
