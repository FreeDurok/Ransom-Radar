import logging
import time
import json
from ransomlook.client import RansomLookClient
from ransomlook.state import RansomLookState
from ransomlook.utils import compute_post_id, format_message
from modules.notifier.telegram import send_message, send_photo
from modules.augmentation.openai_client import OpenAIClient

openai_client = OpenAIClient()

client = RansomLookClient()
state = RansomLookState()


def enrich_post(post):
    ai_info = openai_client.enrich_post(post)
    if not ai_info:
        logging.warning(f"No enrichment data found for victim.")
        return post
    ai_info = json.loads(ai_info)
    post['ai_work_sector'] = ai_info.get('work_sector', None)
    post['ai_description'] = ai_info.get('description', None)
    post['ai_country'] = ai_info.get('country', None)
    return post


def process_new_ransomlook_posts(AI_ENABLED=False):
    
    try:
        posts = client.get_recent_posts()[::-1]
        
        if not posts:
            logging.info("No new posts found.")
            return

        for post in posts:
            post_id = compute_post_id(post)
            if state.is_new(post_id):
                group_name = post.get('group_name', 'Unknown')
                group_info = client.get_group_info(group_name=group_name)
                if AI_ENABLED:
                    post = enrich_post(post)
                msg = format_message(post, group_info)
                try:
                    send_message(msg)
                    if post.get('screen'):
                        try:
                            img_data = client.get_post_screen(post)
                            photo = send_photo(caption=f"🖼 {post.get('post_title')}", img_data=img_data)                            
                        except Exception as e:
                            logging.warning(f"Unable to send screenshot for post {post_id}: {e}")
                    logging.info(f"Sent message for post {post_id}")
                    state.save()
                except Exception as e:
                    if hasattr(e, 'response') and getattr(e.response, 'status_code', None) == 429:
                        logging.warning(f"Rate limited (429 Too Many Requests) for post {post_id}. Sleeping for 60 seconds.")
                        time.sleep(60)
                    else:
                        logging.error(f"Failed to send message for post {post_id}: {e}")
    except Exception as e:
        logging.error(e)