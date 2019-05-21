import os, requests, time, schedule, json

import lib.weatheralertheadlines as alert_headlines
import lib.weatheralertdetails as alert_details
import lib.dailyforecast as daily_forecast
import lib.tropicalforecastprojectedpath as tropical_forecast
import lib.severeweatherpowerdisruptionindex as power_disruption
import paho.mqtt.client as mqtt

from lib.apiutil import request_headers, default_params
from lib.msgutil import create_message

def handleFail(err):
  # API call failed...
  return('Status code: %d' % (err.status_code) )

def callWeatherAlertHeadlines(lat, lon):
  url, params = alert_headlines.request_options(lat, lon)
  headers = request_headers()

  r = requests.get(url, headers=headers)
  if r.status_code == 200:
    detailKeys = alert_headlines.handle_response(r.json())
    if detailKeys and len(detailKeys) > 0:
      for detailKey in detailKeys:
        print('Detail key: '+detailKey)
        callWeatherAlertDetails(detailKey)
  else:
    handleFail(r)

def callWeatherAlertDetails(detailKey):
  url, params = alert_details.request_options(detailKey)
  headers = request_headers()

  r = requests.get(url, headers=headers)
  if r.status_code == 200:
    alert_details.handle_response(r.json())
  else:
    handleFail(r)

def callTropicalForecastProjectedPath(basin='AL', units='m', nautical=True, source='all'):
  url, params = tropical_forecast.request_options(basin, units, nautical, source)
  headers = request_headers()

  r = requests.get(url, headers=headers)
  if r.status_code == 200:
    tropical_forecast.handle_response(r.json())
  else:
    handleFail(r)

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

def callSevereWeatherPowerDisruption(lat, lon):
  url, params = power_disruption.request_options(lat, lon)
  headers = request_headers()

  r = requests.get(url, headers=headers)
  if r.status_code == 200:
    power_disruption.handle_response(r.json())
  else:
    handleFail(r)

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