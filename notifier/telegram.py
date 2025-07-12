import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    resp = requests.post(url, data=data)
    resp.raise_for_status()



def send_photo(caption, img_data):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    files = {'photo': img_data}
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "caption": caption,
        "parse_mode": "HTML"
    }
    resp = requests.post(url, data=data, files=files)
    if not resp.ok:
        print("[ERROR] Failed to send photo:")
    resp.raise_for_status()

