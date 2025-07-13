import httpx
from openai import OpenAI
from config import OPENAI_API_KEY, PROXY_URL

class OpenAIClient:

    def __init__(self, api_key=OPENAI_API_KEY, proxy_url=PROXY_URL):
        if proxy_url:
            self.client = OpenAI(
                api_key=api_key,
                http_client=httpx.Client(proxy=proxy_url)
            )
        else:
            self.client = OpenAI(
                api_key=api_key
            )
        

    def enrich_entity(self, entity_name):
        prompt = (
            f"Given the entity '{entity_name}', provide a precise and factual description including country of origin, annual revenue, number of employees, and whether it is publicly traded. "
            "All these details should be included in the 'description' field. "
            "Respond strictly in JSON format with only the fields: 'description' and 'country'. "
            "Do not include any text outside the JSON."
        )
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
        
