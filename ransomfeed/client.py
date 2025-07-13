import requests

from ransomfeed.config import API_URL, BASE_URL

class RansomFeedClient:

    def __init__(self, base_url=BASE_URL, api_url=API_URL):
        self.base_url = base_url
        self.api_url = api_url


    def get_recent_posts(self):
        resp = requests.get(f"{self.api_url}")
        resp.raise_for_status()
        return resp.json()