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

    msg = f"🚨 <b>New Ransom Post</b> 🚨\n\n" \
        f"🔎 <b>Source: <a href='{BASE_URL}'><u>RansomFeed</u></a></b>\n\n" \
        f"🕷 <b>Ransom Group:\n       <a href='{BASE_URL}/stats.php?page=group-profile&group={group_name}'><u>{group_name.title()}</u></a></b>\n\n" \
        f"☢️​ <b>Victim:</b>\n       <code>{victim}</code>\n" \
        f"🌍 <b>Country:</b>\n       <code>{country}</code>\n" \
        f"📅 <b>Discovered:</b>\n       <code>{discovered} CEST</code>\n"
    
    if website:
        msg += f"🌐 <b>Website:\n       <a href='{website}'><u>{website}</u></a></b>\n"

    if work_sector:
        msg += f"💼 <b>Work Sector:</b>\n       <code>{work_sector}</code>\n"

    if description:
        msg += f"\n📝 <b>Description:</b>\n<code>{description.strip()}</code>\n\n"

    msg += f"🔗  <b><a href='{BASE_URL}/index.php?page=post_details&id_post={id}'><u>Post Details</u></a></b>\n"

    return msg