import requests
import base64

from ransomlook.config import BASE_URL

class RansomLookClient:

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url


    def get_post_screen(self, post):
        screen_url = f"{self.base_url}/{post.get('screen')}"
        resp = requests.get(screen_url)
        resp.raise_for_status()
        return resp.content        


    def get_recent_posts(self):
        resp = requests.get(f"{self.base_url}/api/recent")
        resp.raise_for_status()
        return resp.json()


    def get_group_info(self, group_name):
        resp = requests.get(f"{self.base_url}/api/group/{group_name}")
        resp.raise_for_status()
        location = resp.json()[0]['locations'][0]

        slug = location.get('slug')
        fqdn = location.get('fqdn')
        title = location.get('title') 
        updated = location.get('updated')

        screen_value = resp.json()[0]['locations'][0].get('screen')
        if screen_value:
            screen_data = base64.b64decode(screen_value)
            
        data = {
            "slug": slug,
            "fqdn": fqdn,
            "title": title,
            "updated": updated,
            "screen": screen_data if screen_value else None
        }

        return data