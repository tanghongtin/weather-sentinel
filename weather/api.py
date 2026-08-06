import requests
from datetime import datetime

from config.fields import FIELDS

HOURLY_FIELDS = list(FIELDS.keys())


def get_weather(
    latitude,
    longitude,
    timezone,
    forecast_days=7,
    model="auto"
):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": HOURLY_FIELDS,
        "timezone": timezone,
        "forecast_days": forecast_days
    }

    if model and model.lower() != "auto":
        params["models"] = model

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    #print(data)
    hourly = data["hourly"]

    forecast = []

    total_hours = forecast_days * 24
    for i in range(total_hours):

        hour = {
            "time": datetime.fromisoformat(hourly["time"][i]),
            "temperature": hourly["temperature_2m"][i],
            "probability": hourly["precipitation_probability"][i],
            "rain": hourly["precipitation"][i],
            "cloud_low": hourly["cloud_cover_low"][i],
            "cloud_mid": hourly["cloud_cover_mid"][i],
            "cape": hourly["cape"][i],
            "wind": hourly["wind_speed_10m"][i],
        }

        forecast.append(hour)

    return forecast