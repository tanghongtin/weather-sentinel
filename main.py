import yaml

from weather.api import get_weather
from display.console import (
    show_forecast,
    build_forecast_text,
)

from notifier.telegram import send_message
from dotenv import load_dotenv
import os

load_dotenv()
telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

def load_config():

    with open("config.yaml", "r") as file:

        return yaml.safe_load(file)


def main():

    config = load_config()
    forecast = get_weather(
        latitude=config["latitude"],
        longitude=config["longitude"],
        timezone=config["timezone"],
        forecast_days=config["forecast_days"],
        model=config["model"],
    )

    show_forecast(
    forecast,
    config["display_days"]
    )

    text = build_forecast_text(
        forecast,
        config["display_days"]
    )

    send_message(
        telegram_token,
        telegram_chat_id,
        text,
    )

if __name__ == "__main__":

    main()