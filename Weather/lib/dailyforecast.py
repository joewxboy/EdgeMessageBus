# This Python file uses the following encoding: utf-8

# Daily Forecast
#
# - https://weather.com/swagger-docs/ui/sun/v1/sunV1DailyForecast.json
#
# The daily forecast API returns the geocode weather forecasts for the current day
# up to the days duration in the API endpoint. The daily forecast product can contain
# multiple days of daily forecasts for each location. Each day of a forecast can
# contain up to (3) “temporal segments” meaning three separate forecasts. For any
# given forecast day we offer day, night, and a 24-hour forecast (daily summary).
#
# Base URL: https://twcservice.mybluemix.net/api/weather
# Endpoint: /v1/geocode/{latitude}/{longitude}/forecast/daily/{days}day.json

__name__ = 'dailyforecast'

import json
from lib.apiutil import host, default_params

def request_options (lat, lon, days = 3, units = 'e'):
  d = days if days in [3, 5, 7, 10, 15] else 3
  u = units if units in ['e', 'm', 'h', 's'] else 'e'

  url = host + '/v1/geocode/{lat}/{lon}/forecast/daily/{days}day.json'.format(lat=lat, lon=lon, days=d)
  params = default_params()
  params['units'] = u

  return url, params

def handle_response (res):
  if res and res['forecasts']:
    forecasts = res['forecasts']
    return forecasts
  else:
    print("returning error")
    return json.dumps('daily-forecast: no daily forecast returned')
