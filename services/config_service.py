import os

from dotenv import load_dotenv
import yaml


def load_config():
    load_dotenv()
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    for key in ("latitude", "longitude"):
        value = os.getenv(key.upper())
        if value is None:
            raise ValueError(
                f"Required environment variable {key.upper()} is not set"
            )
        try:
            config[key] = float(value)
        except ValueError as error:
            raise ValueError(
                f"Environment variable {key.upper()} must be a number"
            ) from error

    return config