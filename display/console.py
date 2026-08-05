from datetime import timedelta
from weather.formatter import format_datetime

from config.rules import MIN_RAIN_MM

from config.fields import FIELDS


def build_forecast_text(forecast, display_days):

    lines = []

    end_time = forecast[0]["time"] + timedelta(days=display_days)

    for hour in forecast:

        if hour["time"] >= end_time:
            break

        if hour["rain"] < MIN_RAIN_MM:
            continue

        text = format_datetime(hour["time"])

        for config in FIELDS.values():

            if not config["show"]:
                continue

            value = hour.get(config["key"])

            text += (
                f" | {config['icon']} "
                f"{value}{config['unit']}"
            )

        lines.append(text)

    return "\n".join(lines)


def show_forecast(forecast, display_days):

    print()
    print("=" * 80)
    print("FORECAST")
    print("=" * 80)

    print(build_forecast_text(forecast, display_days))