import httpx
import logging
import json
from openai import OpenAI
from config import PROXY_URL, API_KEY, API_URL, AI_MODEL

class OpenAIClient:

    def __init__(self, base_url=API_URL, api_key=API_KEY, proxy_url=PROXY_URL):

        if api_key and proxy_url:
            self.client = OpenAI(
                base_url=base_url,
                api_key=api_key,
                http_client=httpx.Client(proxy=proxy_url)
            )
        elif api_key:
            self.client = OpenAI(
                base_url=base_url,
                api_key=api_key,
            )
        else:
            self.client = None
        
    def enrich_post(self, post):
        victim = post.get('victim', None)
        country = post.get('country', None)
        website = post.get('website', None)

        # prompt = (
        #     f"Given the entity '{victim}' based in '{country}', provide a precise and factual description including country of origin, work sector, annual revenue, number of employees, and whether it is publicly traded. "
        #     "All these details should be included in the 'description' field. "
        #     "Respond strictly in JSON format with only the fields: 'description', 'work_sector' and 'country'. "
        #     "Do not include any text outside the JSON."   
        # )

        prompt = (
            f"Given the entity '{victim}' based in '{country}' with this website '{website}', provide a recise and factual description including country of origin, work sector, annual revenue, number of employees, and whether it is publicly traded. "
            "If any information is uncertain or unknown, respond with an empty string ('') as the value for that key. "
            "Respond ONLY in JSON with fields: 'description', 'work_sector', 'country'. No extra text."
        )
        response = self.client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )        

        ai_info = response.choices[0].message.content.strip()

        if not ai_info:
            logging.warning(f"No enrichment data found for victim.")
            return post
        ai_info = json.loads(ai_info)
        post['ai_work_sector'] = ai_info.get('work_sector', None)
        post['ai_description'] = ai_info.get('description', None)
        post['ai_country'] = ai_info.get('country', None)

        return post
        
