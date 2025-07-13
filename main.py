import os
import logging
from config import POLL_INTERVAL, LOG_FILE_PATH
from logging.handlers import RotatingFileHandler
from ransomlook.jobs import process_new_ransomlook_posts
from ransomfeed.jobs import process_new_ransomfeed_posts
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

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', seconds=POLL_INTERVAL)
def ransomlook_jobs():
    process_new_ransomlook_posts()


@scheduler.scheduled_job('interval', seconds=POLL_INTERVAL)
def ransomfeed_jobs():
    process_new_ransomfeed_posts()


scheduler.start()