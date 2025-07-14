import logging
import time
import requests
from providers.ransomfeed.config import BASE_URL
from providers.ransomfeed.client import RansomFeedClient
from providers.ransomfeed.state import RansomFeedState
from providers.ransomfeed.utils import format_message
from modules.ai.openai_client import OpenAIClient
from modules.notifier.telegram import send_message 
from modules.formatter.post_formatter import parse_post


openai_client = OpenAIClient()

client = RansomFeedClient()
state = RansomFeedState()


def process_new_ransomfeed_posts(ai_module=False):
    try:
        posts = client.get_recent_posts()[::-1]        
        
        if not posts:
            logging.info("No new posts found.")
            return
        
        for post in posts:
            post_id = post.get('id')
            if state.is_new(post_id):
                post = parse_post(post)
                if ai_module and not "***" in post.get('victim', ''):
                    post = openai_client.enrich_post(post)                                                        
                msg = format_message(post)
                try:
                    send_message(msg)
                    logging.info(f"Sent message for post {post_id} from {BASE_URL}")
                    state.save()
                except Exception as e:
                    if hasattr(e, 'response') and getattr(e.response, 'status_code', None) == 429:
                        logging.warning(f"Rate limited (429 Too Many Requests) for post {post_id}. Sleeping for 60 seconds.")
                        time.sleep(60)
                    else:
                        logging.error(f"Failed to send message for post {post_id}: {e}")
    except Exception as e:
        logging.error(e)