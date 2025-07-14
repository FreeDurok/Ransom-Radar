import logging
import time
import json
import requests
from ransomlive.config import BASE_URL
from ransomlive.client import RansomLiveClient
from ransomlive.state import RansomLiveState
from ransomlive.utils import format_message
from modules.notifier.telegram import send_message, send_photo 
from modules.ai.openai_client import OpenAIClient
from modules.formatter.post_formatter import parse_post


openai_client = OpenAIClient()

client = RansomLiveClient()
state = RansomLiveState()

def check_yara_link(post):
    group = post.get('group', None)
    yara_rules = client.get_yara_by_group(group.title())
    if yara_rules:
        filename = yara_rules['rules'][0].get('filename', None)
        yara_link = f"{BASE_URL}/yara/{group.title()}/{filename}"
        post['yara_link'] = yara_link
        return post
    else:
        logging.warning(f"No YARA rule found for group {group}.")
        return post


def process_new_ransomlive_posts(ai_module=False):
    try:
        posts = client.get_recent_victims()        
        posts = posts.get('victims', [])
        posts = list(reversed(posts))

        if not posts:
            logging.info("No new posts found.")
            return
        
        for post in posts:
            post_id = post.get('id')
            if state.is_new(post_id): 
                post = check_yara_link(post)
                post = parse_post(post)                      
                if ai_module:
                    post = openai_client.enrich_post(post)                                    
                msg = format_message(post)             
                try:
                    send_message(msg)
                    if post.get('screenshot', None):                            
                        try:
                            img_data = client.get_post_screen(post)
                            photo = send_photo(caption=f"🖼 {post.get('victim')}", img_data=img_data)                            
                        except Exception as e:
                            logging.warning(f"Unable to send screenshot for post {post_id}: {e}")
                    logging.info(f"Sent message for post {post_id} from {BASE_URL}")
                    state.save()
                except Exception as e:
                    if hasattr(e, 'response') and getattr(e.response, 'status_code', None) == 429:
                        logging.warning(f"Rate limited (429 Too Many Requests) for post {post_id}. Sleeping for 60 seconds.")
                        time.sleep(60)
                    else:
                        logging.error(f"Failed to send message for post {post_id}: {e}")
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection error: {e}")
        time.sleep(60)
    except Exception as e:
        logging.error(e)