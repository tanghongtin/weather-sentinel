import os

from dotenv import load_dotenv

from display.console import (
    show_forecast,
    build_forecast_text,
)

from services.config_service import load_config
from services.weather_service import get_forecasts
from services.telegram_service import send_forecast

load_dotenv()


def get_runtime():

    return (
        "🚀 GitHub Actions"
        if os.getenv("GITHUB_ACTIONS") == "true"
        else "💻 Local"
    )


def run():

    config = load_config()

    forecasts = get_forecasts(config)

    show_forecast(
        forecasts,
        config["days"],
    )

    text = (
        f"{get_runtime()}\n\n"
        f"{build_forecast_text(
            forecasts,
            config['days'],
        )}"
    )

    send_forecast(text)