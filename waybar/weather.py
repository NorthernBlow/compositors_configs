#!/usr/bin/env python

import json
import requests
from datetime import datetime
import os
import time

WEATHER_CODES = {
    '113': '☀️',
    '116': '⛅️',
    '119': '☁️',
    '122': '☁️',
    '143': '🌫',
    '176': '🌦',
    '179': '🌧',
    '182': '🌧',
    '185': '🌧',
    '200': '⛈',
    '227': '🌨',
    '230': '❄️',
    '248': '🌫',
    '260': '🌫',
    '263': '🌦',
    '266': '🌦',
    '281': '🌧',
    '284': '🌧',
    '293': '🌦',
    '296': '🌦',
    '299': '🌧',
    '302': '🌧',
    '305': '🌧',
    '308': '🌧',
    '311': '🌧',
    '314': '🌧',
    '317': '🌧',
    '320': '🌨',
    '323': '🌨',
    '326': '🌨',
    '329': '❄️',
    '332': '❄️',
    '335': '❄️',
    '338': '❄️',
    '350': '🌧',
    '353': '🌦',
    '356': '🌧',
    '359': '🌧',
    '362': '🌧',
    '365': '🌧',
    '368': '🌨',
    '371': '❄️',
    '374': '🌧',
    '377': '🌧',
    '386': '⛈',
    '389': '🌩',
    '392': '⛈',
    '395': '❄️'
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




for i in range(max_tries):
    if check_ethernet_conn():
        try:
            weather = requests.get(url)
        except requests.exceptions.RequestException as exc:
            #print('Попытка номер{} провалена: {}'.format(i+1, exc))
            time.sleep(5)
        finally:
            if weather.status_code == 200:
                #print('Подключилось успешно')
                break
            if weather.status_code != 200:
                #print('Попытка номер{} провалилась:{}'.format(i+1, weather.status_code))
                time.sleep(2)
    else:
        time.sleep(3)


weather = weather.json()




def format_time(time):
    return time.replace("00", "").zfill(2)


def format_temp(temp):
    return (hour['FeelsLikeC']+"°").ljust(3)


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


waybar_condition: str = ''

match weather['current_condition'][0]['weatherDesc'][0]['value']:

    case 'Partly cloudy':
        waybar_condition = 'broken clouds '
    case 'Sunny':
        waybar_condition = 'another sky is young '
    case 'Mist':
        waybar_condition = 'horizon of ruin '
    case 'Patchy rain':
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
        waybar_congition = 'heavy rain '


data['text'] = waybar_condition + WEATHER_CODES[weather['current_condition'][0]['weatherCode']] + \
    " "+weather['current_condition'][0]['FeelsLikeC']+"°"


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
    data['tooltip'] += f"⬆️ {day['maxtempC']}° ⬇️ {day['mintempC']}° "
    data['tooltip'] += f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"
    for hour in day['hourly']:
        if i == 0:
            if int(format_time(hour['time'])) < datetime.now().hour-2:
                continue
        data['tooltip'] += f"{format_time(hour['time'])} {WEATHER_CODES[hour['weatherCode']]} {format_temp(hour['FeelsLikeC'])} {hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"


print(json.dumps(data))
