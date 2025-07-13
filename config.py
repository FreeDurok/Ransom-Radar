import os
from dotenv import load_dotenv

load_dotenv()

POLL_INTERVAL = 150 # seconds
LOG_FILE_PATH = os.path.expanduser("~/.ransom-radar/ransom_radar.log")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROXY_URL = os.getenv("PROXY_URL", None)