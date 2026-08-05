import yaml

from weather.api import get_weather
from notify.telegram import send_message
from display.console import show_forecast

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

if __name__ == "__main__":

    main()