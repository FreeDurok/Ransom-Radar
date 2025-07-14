import logging
import time
from ransomlook.client import RansomLookClient
from ransomlook.state import RansomLookState
from ransomlook.utils import compute_post_id, format_message
from modules.notifier.telegram import send_message, send_photo
from modules.ai.openai_client import OpenAIClient
from modules.formatter.post_formatter import parse_post


openai_client = OpenAIClient()

client = RansomLookClient()
state = RansomLookState()


def process_new_ransomlook_posts(ai_module=False):
    
    try:
        posts = client.get_recent_posts()[::-1]
        
        if not posts:
            logging.info("No new posts found.")
            return

        for post in posts:
            post = compute_post_id(post)
            post_id = post.get('id')
            if state.is_new(post_id):
                group_name = post.get('group_name', 'Unknown')
                group_info = client.get_group_info(group_name=group_name)
                post = parse_post(post, group_info=group_info)
                if ai_module:
                    post = openai_client.enrich_post(post)
                msg = format_message(post, group_info)
                try:
                    send_message(msg)
                    if post.get('screenshot'):
                        try:
                            img_data = client.get_post_screen(post)
                            photo = send_photo(caption=f"🖼 {post.get('victim')}", img_data=img_data)                            
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