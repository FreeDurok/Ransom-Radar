import hashlib
from ransomlook.config import BASE_URL
from datetime import datetime


def format_date(raw_date):    
    dt = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S.%f")
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def compute_post_id(post):
    key = f"{post.get('post_title', '')}-{post.get('discovered', '')}"
    return hashlib.sha256(key.encode()).hexdigest()


def format_message(post, group_info):    
    group_name = post.get('group_name', 'Unknown').title()
    description = post.get('description', None)
    post_title = post.get('post_title', 'No Title')
    discovered = post.get('discovered', 'N/A')
    fqdn = group_info.get('fqdn', 'unknown.com')
    link = post.get('link', None)
    screen = post.get('screen', None)
    
    msg = f"🚨 <b>New Ransom Post</b> 🚨\n\n" \
        f"🔎 <b>Source: <a href='{BASE_URL}'><u>RansomLook</u></a></b>\n\n" \
        f"🕷 <b>Ransom Group:\n       <a href='{BASE_URL}/group/{group_name}'><u>{group_name}</u></a></b>\n\n" \
        f"☢️​ <b>Victim:</b>\n       <code>{post_title}</code>\n" \
        f"📅 <b>Discovered:</b>\n       <code>{format_date(discovered)} CEST</code>\n\n" \

    if description:
        msg += f"📝 <b>Description:</b>\n<code>{description.strip()}</code>\n\n"

    if link:
        msg += f"🔗 <b>URL:</b>  https://{fqdn}{link}\n\n"
    else:
        msg += f"🔗 <b>URL:</b>  https://{fqdn}\n\n"

    if screen:
        msg += "🖼  <b>Screenshot</b>  ⬇️​\n"

    return msg