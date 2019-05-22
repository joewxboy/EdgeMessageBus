import json

import paho.mqtt.client as mqtt

from msgutil import create_message
from apiutil import default_params
from weatherhat import WeatherHat
from time import sleep

wh = WeatherHat()

icon_dict = [
    "storm", # 0 tornado
    "storm", # tropical storm
    "storm", # hurricane
    ["cloud","storm","raining"], # strong storms
    ["cloud","storm","raining"], # thunderstorms
    ["cloud","raining"], # 5 rain / snow
    ["cloud","raining"], # rain / sleet
    ["cloud","raining"], # wintry mix
    ["cloud","raining"], # freezing drizzle
    ["cloud","raining"], # drizzle
    ["cloud","raining"], # 10 freezing rain
    ["cloud","raining"], # showers
    ["cloud","raining"], # rain
    ["cloud","raining"], # flurries
    ["cloud","raining"], # snow showers
    "raining", # 15 blowing / drifting snow
    ["cloud","raining"], # snow
    ["cloud","raining"], # hail
    ["cloud","raining"], # sleet
    "fog", # blowing dust / sandstorm
    "fog", # 20 foggy
    "fog", # haze
    "fog", # smoke
    "wind", # breezy
    "wind", # windy
    ["wind","raining"], # 25 frigid / ice crystals
    "cloud", # cloudy
    "cloud", # mostly cloudy
    ["cloud","sun"], # mostly cloudy
    "cloud", # partly cloudy
    ["cloud","sun"], # 30 partly cloudy
    "clear", # clear
    "sun", # sunny
    "clear", # fair, mostly clear
    "sun", # fair, mostly sunny
    ["cloud","raining"], # 35 mixed rain and hail
    "sun", # hot
    ["sun","cloud","raining","storm"], # isolated thunderstorms
    ["sun","cloud","raining","storm"], # scattered thunderstorms
    ["cloud","raining"], # scattered showers
    ["cloud","raining"], # 40 heavy rain
    ["cloud","sun","raining"], # scattered show showers
    ["cloud","raining"], # heavy snow
    ["cloud","raining"], # blizzard
    ["n/a"], # not available
    ["cloud","raining"], # 45 scattered showers
    ["cloud","raining"], # scattered snow showers
    ["cloud","raining","storm"] # scattered thunderstorms
]

def display_condition(condition):
    if(condition == "sun"):
        wh.sun("start")
        sleep(5)
        wh.sun("stop")
        return "Showing sun", 200
    elif(condition == "cloud"):
        wh.cloud("start")
        sleep(5)
        wh.cloud("stop")
        return "Showing cloud", 200
    elif(condition == "raining"):
        wh.raining("start")
        sleep(5)
        wh.raining("stop")
        return "Showing raining", 200
    elif(condition == "storm"):
        wh.storm("start")
        sleep(5)
        wh.storm("stop")
        return "Showing storm", 200
    elif(condition == "rainbow"):
        wh.rainbow("start")
        sleep(5)
        wh.rainbow("stop")
        return "Showing rainbow", 200
    else:
        return "Condition not found", 404

########################
# Connect to MQTT
########################
def on_connect(client, userdata, flags, rc):
  params = default_params()
  client.subscribe(params['mqttTopic'])

def on_message(client, userdata, msg):
  params = default_params()
  shortcast = ""
  iconcode = "44" ## n/a icon
  # print(msg.topic+" "+str(msg.payload))
  str_payload = json.loads(msg.payload)
  if str_payload["type"] == "weather":
    cond = str_payload["data"][0]
    
    if cond["day"]:
        shortcast = cond["day"]["shortcast"]
        iconcode = cond["day"]["icon_code"]
    elif cond["night"]:
        shortcast = cond["night"]["shortcast"]
        iconcode = cond["night"]["icon_code"]
    
    icon_cond = icon_dict[iconcode]
    
    if type(icon_cond) == "str":
        display_condition(icon_cond)
        msgPayload = create_message("display", icon_cond, "")
        # print("sending payload")
        client.publish(params['mqttTopic'], msgPayload, qos=0, retain=False)
    elif type(icon_cond) == "list":
        for icon in icon_cond:
            display_condition(icon)
            msgPayload = create_message("display", icon, "")
            # print("sending payload")
            client.publish(params['mqttTopic'], msgPayload, qos=0, retain=False)
    

params = default_params()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(params['mqttUsername'], params['mqttPassword'])
client.connect(params['mqttBroker'], 1883, 60)
client.loop_forever()