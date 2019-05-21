import os, requests, time, schedule, json

import dailyforecast as daily_forecast
import paho.mqtt.client as mqtt

from apiutil import request_headers, default_params
from msgutil import create_message

def handleFail(err):
  # API call failed...
  return('Status code: %d' % (err.status_code) )

def callDailyForecast(lat, lon, units = 'm'):
  url, params = daily_forecast.request_options(lat, lon)
  headers = request_headers()
  # print("callDailyForecast for {}, {}".format(lat, lon))
  # print(url)

  r = requests.get(url, headers=headers)
  if r.status_code == 200:
    # print("got 200")
    return daily_forecast.handle_response(r.json())
  else:
    # print("got error")
    return handleFail(r)

loc = {
  'boston': { 'lat': '42.36', 'lon': '-71.06' }, # Boston, MA, United States
  'raleigh': { 'lat': '35.84', 'lon': '-78.78' }, # Raleigh, NC, United States
  'losangeles': { 'lat': '34.04', 'lon': '-118.48' }, # Los Angeles, CA, United States
  'lakecity': { 'lat': '44.44', 'lon': '-92.26' }, # Lake CIty, MN, United States
  'newyork': { 'lat': '40.74', 'lon': '-73.98' }, # New York, NY, United States
  'hawaii': { 'lat': '33.40', 'lon': '-83.42' }, # Hawaii, United States
  'puntacana': { 'lat': '18.57', 'lon': '-68.36' }, # Punta Cana, Dominican Republic
  'jakarta': { 'lat': '-5.77', 'lon': '106.11' }, # Jakarta, Indonesia
  'taipei': { 'lat': '25.05', 'lon': '121.53' }, # Taipei, Taiwan, ROC
  'acworth': { 'lat': '34.07', 'lon': '-84.68' }, # Acworth, Georgia
  'marietta': { 'lat': '33.95', 'lon': '-84.55' }, # Marietta, Georgia
  'kennesaw': { 'lat': '34.02', 'lon': '-84.62' } # Kennesaw, Georgia
}

########################
# Connect to MQTT
########################
def on_connect(client, userdata, flags, rc):
  params = default_params()
  client.subscribe(params['mqttTopic'])

def on_message(client, userdata, msg):
  params = default_params()
  # print(msg.topic+" "+str(msg.payload))
  str_payload = json.loads(msg.payload)
  if str_payload["type"] == "location":
    lat = str_payload["data"]["lat"]
    lon = str_payload["data"]["lon"]
    msgJSON = callDailyForecast(lat, lon)
    msgPayload = create_message("weather", json.dumps(msgJSON), "")
    # print("sending payload")
    client.publish(params['mqttTopic'], msgPayload, qos=0, retain=False)

params = default_params()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(params['mqttUsername'], params['mqttPassword'])
client.connect(params['mqttBroker'], 1883, 60)
client.loop_forever()