import os
from dotenv import load_dotenv

load_dotenv()

POLL_INTERVAL = 10 # seconds
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LOG_FILE_PATH = os.path.expanduser("~/.ransom-radar/ransom_radar.log")
