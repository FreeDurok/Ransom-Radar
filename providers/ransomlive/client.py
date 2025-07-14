import requests
from providers.ransomlive.config import API_URL, BASE_URL, API_TOKEN

class RansomLiveClient:
    def __init__(self, base_url=BASE_URL, api_url=API_URL):
        if not API_TOKEN:
            raise ValueError("API_TOKEN must be set in the ransomlive/.env or config file.")
        self.base_url = base_url
        self.api_url = api_url
        self.headers = {
            "Accept": "application/json",
            "X-API-KEY": API_TOKEN  # Set your API key here or provide a setter method
        }

    def get_8k10s(self):
        resp = requests.get(f"{self.api_url}/8k10s", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_csirt_by_country(self, country):
        resp = requests.get(f"{self.api_url}/csirt/{country}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_groups(self):
        resp = requests.get(f"{self.api_url}/groups", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_group_by_name(self, groupname):
        resp = requests.get(f"{self.api_url}/groups/{groupname}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_iocs(self):
        resp = requests.get(f"{self.api_url}/iocs", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_iocs_by_group(self, group):
        resp = requests.get(f"{self.api_url}/iocs/{group}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def list_sectors(self):
        resp = requests.get(f"{self.api_url}/listsectors", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_negotiations(self):
        resp = requests.get(f"{self.api_url}/negotiations", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_negotiations_by_group(self, group):
        resp = requests.get(f"{self.api_url}/negotiations/{group}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_negotiation_chat(self, group, chat_id):
        resp = requests.get(f"{self.api_url}/negotiations/{group}/{chat_id}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_press_all(self):
        resp = requests.get(f"{self.api_url}/press/all", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_press_recent(self):
        resp = requests.get(f"{self.api_url}/press/recent", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_ransomnotes(self):
        resp = requests.get(f"{self.api_url}/ransomnotes", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_ransomnotes_by_group(self, group):
        resp = requests.get(f"{self.api_url}/ransomnotes/{group}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_ransomnote_detail(self, group, note_name):
        resp = requests.get(f"{self.api_url}/ransomnotes/{group}/{note_name}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_stats(self):
        resp = requests.get(f"{self.api_url}/stats", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def validate(self):
        resp = requests.get(f"{self.api_url}/validate", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_victim(self, victim_id):
        resp = requests.get(f"{self.api_url}/victim/{victim_id}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_victims(self):
        resp = requests.get(f"{self.api_url}/victims", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_recent_victims(self):
        resp = requests.get(f"{self.api_url}/victims/recent?order=discovered", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def search_victims(self):
        resp = requests.get(f"{self.api_url}/victims/search", headers=self.headers)
        resp.raise_for_status()
        return resp.json() 

    def get_yara(self):
        resp = requests.get(f"{self.api_url}/yara", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_yara_by_group(self, group):
        resp = requests.get(f"{self.api_url}/yara/{group}", headers=self.headers)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

    def get_post_screen(self, post):
        screen_url = f"{post.get('screenshot')}"
        resp = requests.get(screen_url)
        resp.raise_for_status()
        return resp.content        
