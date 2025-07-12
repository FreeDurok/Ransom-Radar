import hashlib
from datetime import datetime

def format_date(raw_date):    
    dt = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S.%f")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def compute_post_id(post):
    key = f"{post.get('post_title', '')}-{post.get('discovered', '')}"
    return hashlib.sha256(key.encode()).hexdigest()

def format_message(post, group_info):
    
    msg = f"🚨 <b>New Ransomware Post!</b> 🚨\n\n" \
        f"🕷 <b>Ransom Group:</b>  <code>{post.get('group_name')}</code>\n\n" \
        f"☢️​ <b>Victim:</b>  <code>{post.get('post_title')}</code>\n" \
        f"📅 <b>Discovered:</b>  <code>{format_date(post.get('discovered'))}</code>\n\n" \
        # f"🔗 <b>Group URL:</b> https://{group_info.get('fqdn')}\n" \
        # f"⏰ <b>Group Updated:</b> {format_date(group_info.get('updated', 'N/A'))}\n\n" \
    
    if post.get('description'):
        msg += f"📝 <b>Description:</b>\n<code>{post.get('description').strip()}</code>\n\n"

    if post.get('link'):
        msg += f"🔗 <b>URL:</b>  https://{group_info.get('fqdn')}{post.get('link')}\n"
    else:
        msg += f"🔗 <b>URL:</b>  https://{group_info.get('fqdn')}\n"

    return msg