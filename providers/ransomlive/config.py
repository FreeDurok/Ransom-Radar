from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="providers/ransomlive/.env")

API_TOKEN = os.getenv("API_TOKEN")

API_URL = "https://api-pro.ransomware.live"
BASE_URL = "https://www.ransomware.live" 
CACHE_DIR = "providers/ransomlive/.cache"

