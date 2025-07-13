from ransomfeed.config import BASE_URL


def format_message(post):
    id = post.get('id', 'Unknown')
    group_name = post.get('gang', 'Unknown')
    victim = post.get('victim', 'No Title')
    discovered = post.get('date', 'N/A')
    country = post.get('country', 'Unknown')
    description = post.get('description', None)
    work_sector = post.get('work_sector', None)
    website = post.get('website', None)

    msg = f"🚨 <b>New Ransomware Post from <a href='{BASE_URL}'>RansomFeed</a>!</b> 🚨\n\n" \
        f"🕷 <b>Ransom Group:</b>\n       <a href='{BASE_URL}/stats.php?page=group-profile&group={group_name}'>{group_name.title()}</a>\n\n" \
        f"☢️​ <b>Victim:</b>\n       <code>{victim}</code>\n" \
        f"🌍 <b>Country:</b>\n       <code>{country}</code>\n" \
        f"📅 <b>Discovered:</b>\n       <code>{discovered} CEST</code>\n\n"
    
    if website:
        msg += f"🌐 <b>Website:</b>\n       <code>{website}</code>\n"

    if work_sector:
        msg += f"💼 <b>Work Sector:</b>\n       <code>{work_sector}</code>\n\n"

    if description:
        msg += f"📝 <b>Description:</b>\n<code>{description.strip()}</code>\n\n"

    msg += f"🔗  <b><a href='{BASE_URL}/index.php?page=post_details&id_post={id}'>Post Details</a></b>\n"

    return msg