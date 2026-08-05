import requests
from datetime import datetime

from config.fields import FIELDS
from config.rules import MIN_RAIN_MM

HOURLY_FIELDS = list(FIELDS.keys())


def get_weather(
    latitude,
    longitude,
    timezone,
    forecast_days=7,
    model="best_match"
):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": HOURLY_FIELDS,
        "timezone": timezone,
        "forecast_days": forecast_days,
        "models": model
        
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    data = response.json()
    hourly = data["hourly"]

    forecast = []

    total_hours = len(hourly["time"]) - 96
    for i in range(total_hours):

        hour = {
            "time": datetime.fromisoformat(hourly["time"][i]),
            "temperature": hourly["temperature_2m"][i],
            "probability": hourly["precipitation_probability"][i],
            "rain": hourly["precipitation"][i],
            "cloud": hourly["cloud_cover"][i],
            "wind": hourly["wind_speed_10m"][i],
        }

        forecast.append(hour)

    return forecast