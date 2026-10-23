from weather.api import get_weather


def get_forecasts(config):
    return get_weather(
        latitude=config["latitude"],
        longitude=config["longitude"],
        timezone=config["timezone"],
        forecast_days=config["days"],
        model=config["model"],
    )