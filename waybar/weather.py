#!/usr/bin/env python

import json
import requests
from datetime import datetime

# Belgorod coordinates
LAT = 50.5958
LON = 36.5873

# WMO weather code → (nerd font icon, description, short description)
WMO_CODES = {
    0:  ('', 'Clear sky', 'perfect dark'),
    1:  ('', 'Mainly clear', 'another sky is young'),
    2:  ('', 'Partly cloudy', 'broken clouds'),
    3:  ('', 'Overcast', 'sky is falling'),
    45: ('', 'Fog', 'fog'),
    48: ('', 'Freezing fog', 'white frost'),
    51: ('', 'Light drizzle', 'blind light'),
    53: ('', 'Moderate drizzle', 'blind light'),
    55: ('', 'Dense drizzle', 'blind light'),
    56: ('', 'Freezing drizzle', 'white frost'),
    57: ('', 'Heavy freezing drizzle', 'white frost'),
    61: ('', 'Slight rain', 'filthy rain'),
    63: ('', 'Moderate rain', 'filthy rain'),
    65: ('', 'Heavy rain', 'heavy rain'),
    66: ('', 'Freezing rain', 'acid rain'),
    67: ('', 'Heavy freezing rain', 'acid rain'),
    71: ('', 'Slight snow', 'white silence'),
    73: ('', 'Moderate snow', 'snow storm'),
    75: ('', 'Heavy snow', 'snow storm'),
    77: ('', 'Snow grains', 'white silence'),
    80: ('', 'Slight showers', 'risk of rain'),
    81: ('', 'Moderate showers', 'risk of rain'),
    82: ('', 'Violent showers', 'heavy rain'),
    85: ('', 'Snow showers', 'white silence'),
    86: ('', 'Heavy snow showers', 'snow storm'),
    95: ('', 'Thunderstorm', 'thunderstorm'),
    96: ('', 'Thunderstorm w/ hail', 'thunderstorm'),
    99: ('', 'Thunderstorm w/ heavy hail', 'thunderstorm'),
}

url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&current=temperature_2m,apparent_temperature,weather_code,"
    "wind_speed_10m,relative_humidity_2m"
    "&daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset"
    "&timezone=Europe/Moscow&forecast_days=3"
)

data = {}

try:
    resp = requests.get(url, timeout=8)
    resp.raise_for_status()
    w = resp.json()
except Exception as e:
    data['text'] = " N/A"
    data['tooltip'] = f"Weather unavailable: {e}"
    print(json.dumps(data))
    exit()

cur = w['current']
daily = w['daily']

code = cur['weather_code']
icon, desc, short = WMO_CODES.get(code, ('', 'Unknown', 'unknown'))

temp = cur['temperature_2m']
feels = cur['apparent_temperature']
wind = cur['wind_speed_10m']
humidity = cur['relative_humidity_2m']

data['text'] = f"{short} {icon} {feels:.0f}°"

tooltip = f"<b>{desc} {temp:.0f}°</b>\n"
tooltip += f"Feels like: {feels:.0f}°\n"
tooltip += f"Wind: {wind:.0f} km/h\n"
tooltip += f"Humidity: {humidity:.0f}%\n"

day_names = ['Today', 'Tomorrow', 'Day after']
for i in range(len(daily['time'])):
    d_code = daily['weather_code'][i]
    d_icon, d_desc, _ = WMO_CODES.get(d_code, ('', 'Unknown', ''))
    tmax = daily['temperature_2m_max'][i]
    tmin = daily['temperature_2m_min'][i]
    sunrise = daily['sunrise'][i][11:]  # HH:MM
    sunset = daily['sunset'][i][11:]
    label = day_names[i] if i < len(day_names) else daily['time'][i]
    tooltip += f"\n<b>{label}, {daily['time'][i]}</b>\n"
    tooltip += f" {tmax:.0f}°   {tmin:.0f}°   {d_icon} {d_desc}\n"
    tooltip += f"  {sunrise}   {sunset}\n"

data['tooltip'] = tooltip
print(json.dumps(data))
