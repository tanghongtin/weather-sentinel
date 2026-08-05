from weather.api import get_weather


def get_forecasts(config):

    forecasts = {}

    for model in config["models"]:

        forecasts[model] = get_weather(
            latitude=config["latitude"],
            longitude=config["longitude"],
            timezone=config["timezone"],
            forecast_days=config["days"],
            model=model,
        )

    return forecasts