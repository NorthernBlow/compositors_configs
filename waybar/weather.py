#!/usr/bin/env python

import json
import requests
from datetime import datetime
import time

# Nerd Font weather icons (nf-weather-*)
WEATHER_CODES = {
    '113': '',   # sunny/clear
    '116': '',   # partly cloudy
    '119': '',   # cloudy
    '122': '',   # overcast
    '143': '',   # fog
    '176': '',   # rain
    '179': '',   # sleet
    '182': '',   # sleet
    '185': '',   # sleet
    '200': '',   # thunderstorm
    '227': '',   # snow
    '230': '',   # snow heavy
    '248': '',   # fog
    '260': '',   # fog
    '263': '',   # light rain
    '266': '',   # light rain
    '281': '',   # sleet
    '284': '',   # sleet
    '293': '',   # light rain
    '296': '',   # rain
    '299': '',   # rain
    '302': '',   # rain heavy
    '305': '',   # rain heavy
    '308': '',   # rain heavy
    '311': '',   # sleet
    '314': '',   # sleet
    '317': '',   # sleet
    '320': '',   # snow
    '323': '',   # snow
    '326': '',   # snow
    '329': '',   # snow heavy
    '332': '',   # snow heavy
    '335': '',   # snow heavy
    '338': '',   # snow heavy
    '350': '',   # hail
    '353': '',   # rain
    '356': '',   # rain heavy
    '359': '',   # rain heavy
    '362': '',   # sleet
    '365': '',   # sleet
    '368': '',   # snow
    '371': '',   # snow heavy
    '374': '',   # hail
    '377': '',   # hail
    '386': '',   # thunderstorm
    '389': '',   # thunderstorm
    '392': '',   # thunderstorm
    '395': ''    # snow heavy
}

data = {}

def check_ethernet_conn():
    try:
        res = requests.get("https://ya.ru", timeout=3)
        return True
    except requests.ConnectionError:
        return False

url = "https://wttr.in/?format=j1"
max_tries = 10

weather = None
for i in range(max_tries):
    if check_ethernet_conn():
        try:
            weather = requests.get(url, timeout=10)
            if weather.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(5)
    else:
        time.sleep(3)

if weather is None or weather.status_code != 200:
    data['text'] = " N/A"
    data['tooltip'] = "Weather unavailable"
    print(json.dumps(data))
    exit()

weather = weather.json()

def format_time(time):
    return time.replace("00", "").zfill(2)

def format_temp(temp):
    return (temp+"°").ljust(3)

def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }
    conditions = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(chances[event]+" "+hour[event]+"%")
    return ", ".join(conditions)

waybar_condition = ''
match weather['current_condition'][0]['weatherDesc'][0]['value']:
    case 'Partly cloudy':
        waybar_condition = 'broken clouds '
    case 'Sunny':
        waybar_condition = 'another sky is young '
    case 'Mist':
        waybar_condition = 'horizon of ruin '
    case 'Patchy rain' | 'Patchy rain possible':
        waybar_condition = 'risk of rain '
    case 'Fog':
        waybar_condition = 'fog '
    case 'Freezing fog':
        waybar_condition = 'white frost '
    case 'Light rain shower':
        waybar_condition = 'acid rain '
    case 'Overcast':
        waybar_condition = 'sky is falling '
    case 'Clear':
        waybar_condition = 'perfect dark '
    case 'Light rain':
        waybar_condition = 'filthy rain '
    case 'Light drizzle':
        waybar_condition = 'blind light '
    case 'Moderate or heavy rain shower':
        waybar_condition = 'heavy rain '
    case 'Light snow' | 'Patchy light snow':
        waybar_condition = 'white silence '
    case 'Moderate snow' | 'Heavy snow':
        waybar_condition = 'snow storm '
    case _:
        waybar_condition = weather['current_condition'][0]['weatherDesc'][0]['value'].lower() + ' '

weather_code = weather['current_condition'][0]['weatherCode']
icon = WEATHER_CODES.get(weather_code, '')

data['text'] = waybar_condition + icon + " " + weather['current_condition'][0]['FeelsLikeC'] + "°"

data['tooltip'] = f"<b>{weather['current_condition'][0]['weatherDesc'][0]['value']} {weather['current_condition'][0]['temp_C']}°</b>\n"
data['tooltip'] += f"Feels like: {weather['current_condition'][0]['FeelsLikeC']}°\n"
data['tooltip'] += f"Wind: {weather['current_condition'][0]['windspeedKmph']}Km/h\n"
data['tooltip'] += f"Humidity: {weather['current_condition'][0]['humidity']}%\n"

for i, day in enumerate(weather['weather']):
    data['tooltip'] += f"\n<b>"
    if i == 0:
        data['tooltip'] += "Today, "
    if i == 1:
        data['tooltip'] += "Tomorrow, "
    data['tooltip'] += f"{day['date']}</b>\n"
    data['tooltip'] += f" {day['maxtempC']}°  {day['mintempC']}° "
    data['tooltip'] += f" {day['astronomy'][0]['sunrise']}  {day['astronomy'][0]['sunset']}\n"
    for hour in day['hourly']:
        if i == 0:
            if int(format_time(hour['time'])) < datetime.now().hour - 2:
                continue
        hour_icon = WEATHER_CODES.get(hour['weatherCode'], '')
        data['tooltip'] += f"{format_time(hour['time'])} {hour_icon} {format_temp(hour['FeelsLikeC'])} {hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"

print(json.dumps(data))
