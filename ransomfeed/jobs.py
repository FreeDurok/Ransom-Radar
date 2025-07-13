import logging
import time
from ransomfeed.client import RansomFeedClient
from ransomfeed.state import RansomFeedState
from ransomfeed.utils import format_message
from notifier.telegram import send_message 


client = RansomFeedClient()
state = RansomFeedState()


def process_new_ransomfeed_posts():
    try:
        posts = client.get_recent_posts()[::-1]        
        
        if not posts:
            logging.info("No new posts found.")
            return
        
        for post in posts:
            post_id = post.get('id')
            if state.is_new(post_id):                
                msg = format_message(post)
                try:
                    send_message(msg)
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