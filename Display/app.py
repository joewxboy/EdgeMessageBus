import json

import paho.mqtt.client as mqtt

from msgutil import create_message
from apiutil import default_params
from weatherhat import WeatherHat
from time import sleep

wh = WeatherHat()

icon_dict = [
    "storm",                           #  0 tornado
    "storm",                           #  1 tropical storm
    "storm",                           #  2 hurricane
    ["cloud","storm","raining"],       #  3 strong storms
    ["cloud","storm","raining"],       #  4 thunderstorms
    ["cloud","raining"],               #  5 rain / snow
    ["cloud","raining"],               #  6 rain / sleet
    ["cloud","raining"],               #  7 wintry mix
    ["cloud","raining"],               #  8 freezing drizzle
    ["cloud","raining"],               #  9 drizzle
    ["cloud","raining"],               # 10 freezing rain
    ["cloud","raining"],               # 11 showers
    ["cloud","raining"],               # 12 rain
    ["cloud","raining"],               # 13 flurries
    ["cloud","raining"],               # 14 snow showers
    "raining",                         # 15 blowing / drifting snow
    ["cloud","raining"],               # 16 snow
    ["cloud","raining"],               # 17 hail
    ["cloud","raining"],               # 18 sleet
    "fog",                             # 19 blowing dust / sandstorm
    "fog",                             # 20 foggy
    "fog",                             # 21 haze
    "fog",                             # 22 smoke
    "wind",                            # 23 breezy
    "wind",                            # 24 windy
    ["wind","raining"],                # 25 frigid / ice crystals
    "cloud",                           # 26 cloudy
    "cloud",                           # 27 mostly cloudy
    ["cloud","sun"],                   # 28 mostly cloudy
    "cloud",                           # 29 partly cloudy
    ["cloud","sun"],                   # 30 partly cloudy
    "clear",                           # 31 clear
    "sun",                             # 32 sunny
    "clear",                           # 33 fair, mostly clear
    "sun",                             # 34 fair, mostly sunny
    ["cloud","raining"],               # 35 mixed rain and hail
    "sun",                             # 36 hot
    ["sun","cloud","raining","storm"], # 37 isolated thunderstorms
    ["sun","cloud","raining","storm"], # 38 scattered thunderstorms
    ["cloud","raining"],               # 39 scattered showers
    ["cloud","raining"],               # 40 heavy rain
    ["cloud","sun","raining"],         # 41 scattered show showers
    ["cloud","raining"],               # 42 heavy snow
    ["cloud","raining"],               # 43 blizzard
    ["n/a"],                           # 44 not available
    ["cloud","raining"],               # 45 scattered showers
    ["cloud","raining"],               # 46 scattered snow showers
    ["cloud","raining","storm"]        # 47 scattered thunderstorms
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
  # print(msg.topic)
  str_payload = json.loads(msg.payload)
  if str_payload["type"] == "weather":
    cond = str_payload["data"][0]
    # print(cond)
    if cond["day"]:
        shortcast = cond["day"]["shortcast"]
        iconcode = cond["day"]["icon_code"]
    elif cond["night"]:
        shortcast = cond["night"]["shortcast"]
        iconcode = cond["night"]["icon_code"]
    print(shortcast)
    print(iconcode)
    icon_cond = icon_dict[iconcode]
    # print(type(icon_cond))
    if type(icon_cond) == basestring:
        display_condition(icon_cond)
        msgPayload = create_message("display", icon_cond, "")
        print("sending payload for "+icon_cond)
        client.publish(params['mqttTopic'], msgPayload, qos=0, retain=False)
    elif type(icon_cond) == list:
        for icon in icon_cond:
            display_condition(icon)
            msgPayload = create_message("display", icon, "")
            print("sending payload for "+icon)
            client.publish(params['mqttTopic'], msgPayload, qos=0, retain=False)
    
params = default_params()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(params['mqttUsername'], params['mqttPassword'])
client.connect(params['mqttBroker'], 1883, 60)
client.loop_forever()