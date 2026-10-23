import requests

def send_message(token, chat_id, text):

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    response = requests.post(url, data=payload)

    response.raise_for_status()


def send_photo(
    token,
    chat_id,
    photo_path,
    caption=""
):

    url = f"https://api.telegram.org/bot{token}/sendPhoto"

    with open(photo_path, "rb") as photo:

        response = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "caption": caption,
            },
            files={
                "photo": photo,
            },
        )

    response.raise_for_status()