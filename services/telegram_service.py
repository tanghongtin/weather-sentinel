import os

from notifier.telegram import send_message


def send_forecast(text):

    send_message(
        os.getenv("TELEGRAM_TOKEN"),
        os.getenv("TELEGRAM_CHAT_ID"),
        text,
    )