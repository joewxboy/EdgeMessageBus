import os

__name__ = 'apiutil'

def default_params():
  return {
    'mqttBroker': os.environ['MQTT_BROKER'],
    'mqttUsername': os.environ['MQTT_USERNAME'],
    'mqttPassword': os.environ['MQTT_PASSWORD'],
    'mqttTopic': os.environ['MQTT_TOPIC']
  }