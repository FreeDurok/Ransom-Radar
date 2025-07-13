import os
import time
import logging
from config import BASE_URL, POLL_INTERVAL, LOG_FILE_PATH
from logging.handlers import RotatingFileHandler
from ransomlook.client import RansomLookClient
from ransomlook.state import State
from ransomlook.utils import compute_post_id, format_message
from notifier.telegram import send_message, send_photo
from apscheduler.schedulers.blocking import BlockingScheduler

if not os.path.exists(os.path.dirname(LOG_FILE_PATH)):
    os.makedirs(os.path.dirname(LOG_FILE_PATH))

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s:  %(message)s',
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(LOG_FILE_PATH, maxBytes=5_000_000, backupCount=5, encoding="utf-8")    
    ]
)

client = RansomLookClient(BASE_URL)
state = State()


scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', seconds=POLL_INTERVAL)
def process_new_posts():
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

scheduler.start()