import os
from dotenv import load_dotenv

load_dotenv()

# Configuration for Ransom Radar
POLL_INTERVAL = 150 # seconds
LOG_FILE_PATH = os.path.expanduser("~/.ransom-radar/ransom_radar.log")

# Telegram Bot Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# AI Configuration
AI_ENABLED = True

# OpenAI Configuration
# API_KEY = os.getenv("OPENAI_API_KEY")
# API_URL = ""
# AI_MODEL="gpt-4",

# Hugging Face Token for Novita Inference API
API_KEY = os.getenv("HF_API_KEY", None)
API_URL = "https://router.huggingface.co/novita/v3/openai"
AI_MODEL = "moonshotai/kimi-k2-instruct"
# AI_MODEL="deepseek/deepseek-r1-0528",

# Proxy Configuration
PROXY_URL = os.getenv("PROXY_URL", None)