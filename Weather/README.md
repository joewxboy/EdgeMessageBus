# Weather Service

## Details

This creates a Docker image for a service that uses The Weather Company Data API. 

This service contains a basic data access application that continuously runs in the background, 
processing a variety of weather data from The Weather Company Data for IBM REST API endpoints, 
to find conditions over time.  It listens for locations or actions from 
a pre-configured MQTT Topic, and responds with the appropriate weather data
in a [weather object](../examples/weather.json) to that Topic.

## Prerequisites

### Obtain a Weather Company API Key

Sign up for [IBM Cloud](https://cloud.ibm.com/login) and 
provision the [Weather Company Data service](https://cloud.ibm.com/catalog/services/weather-company-data). 
The Weather Company Data service uses the following [APIs](https://twcservice.mybluemix.net/rest-api/). 
You can reference [the documentation here](https://cloud.ibm.com/docs/services/Weather?topic=weather-insights_weather_overview).

## Getting Started on your local machine

1. Clone this repository

   ``` bash
   $ git clone https://github.ibm.com/joe-pearson/weather-python-api2mqtt.git
   $ cd weather-python-api2mqtt
   ```  

2. Install the dependencies

   ``` bash
   $ pip3 install -r requirements.txt
   ```

3. Set your Weather API key `<YOUR_API_KEY>` and credentials `<YOUR_API_PASSWORD>` when running the application

   ``` bash
   $ export WEATHER_API_KEY=<YOUR_API_KEY>
   $ export WEATHER_API_URL=https://<YOUR_API_KEY>:<YOUR_API_PASSWORD>@twcservice.mybluemix.net/api/weather
   $ export MQTT_USERNAME=<YOUR_MQTT_USERNAME>
   $ export MQTT_PASSWORD=<YOUR_MQTT_PASSWORD>
   $ export MQTT_TOPIC=<YOUR_MQTT_TOPIC>
   $ export MQTT_BROKER=<YOUR_MQTT_BROKER_URL>
   $ python3 app.py
   ```

4. Publish a location JSON Object to the MQTT Topic and watch the app respond with the weather forecast

    ``` json
    {
        "type":"location",
        "loctype":"geocode",
        "data":{
            "lat":"34.02",
            "lon":"-84.62"
        },
        "child":[]
    }
    ```

## License

This code is licensed under Apache 2.0. Full license text is available in [LICENSE](https://github.com/Call-for-Code/weather-api-python/tree/master/LICENSE).

## Attribution

This code is based on the original work of [krook](https://github.com/krook) in the [`weather-api-python`](https://github.com/Call-for-Code/weather-api-python) repo, as well as substantial refactoring by [vabarbosa](https://github.com/vabarbosa) in his [fork](https://github.com/vabarbosa/weather-api-python).  It would not be possible without their contributions.