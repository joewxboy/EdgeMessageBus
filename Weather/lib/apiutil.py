import os

__name__ = 'dailyforecast'

host = os.environ['WEATHER_API_URL']

def default_params():
  return {
    'apiKey': os.environ['WEATHER_API_KEY'],
    'language': 'en-US',
    'mqttBroker': os.environ['MQTT_BROKER'],
    'mqttUsername': os.environ['MQTT_USERNAME'],
    'mqttPassword': os.environ['MQTT_PASSWORD'],
    'mqttTopic': os.environ['MQTT_TOPIC']
  }

def request_headers():
  return {
    'User-Agent': 'Request-Promise',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip'
  }
