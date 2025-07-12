import time
import logging
from config import BASE_URL, POLL_INTERVAL
from ransomlook.client import RansomLookClient
from ransomlook.state import State
from notifier.telegram import send_message, send_photo
from ransomlook.utils import compute_post_id, format_message

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ransom_alert.log", encoding="utf-8")
    ]
)

client = RansomLookClient(BASE_URL)
state = State()

while True:
    try:
        posts = client.get_recent_posts()[::-1]
        
        if not posts:
            logging.info("No new posts found.")
            time.sleep(POLL_INTERVAL)
            continue      

        for post in posts:                              
            post_id = compute_post_id(post)
            if state.is_new(post_id):
                group_name = post.get('group_name', 'Unknown')
                group_info = client.get_group_info(group_name=group_name)
                msg = format_message(post, group_info)                
                if post.get('screen'):
                    send_message(msg)
                    try:
                        img_data = client.get_post_screen(post)
                        photo = send_photo(caption=post.get('post_title'), img_data=img_data)
                    except Exception as e:
                        logging.warning(f"Unable to send screenshot for post {post_id}: {e}")

    except Exception as e:
        logging.error(e)
    time.sleep(POLL_INTERVAL)
