

def parse_post(post, group_info=None):
    group_info = group_info or {}
    post = {
        "id": post.get("id", "Unknown"),
        "group_name": post.get("gang") or post.get("group") or post.get("group_name", "Unknown"),
        "victim": post.get("victim") or post.get("post_title", "No Title"),
        "discovered": post.get("date") or post.get("discovered", "N/A"),
        "attack_date": post.get("attackdate", None),
        "country": post.get("country", "Unknown"),
        "work_sector": post.get("work_sector", None),
        "description": post.get("description", None),
        "website": post.get("website", None),
        "ai_work_sector": post.get("ai_work_sector", None),
        "ai_description": post.get("ai_description", None),
        "ai_country": post.get("ai_country", "Unknown"),
        "yara_link": post.get("yara_link", None),
        "post_url": post.get("post_url", None),
        "permalink": post.get("permalink", None),
        "press": post.get("press", None),
        "screenshot": post.get("screenshot", None) or post.get("screen", None),
        "post_title": post.get("post_title", None),
        "link": post.get("link", None),
        "fqdn": group_info.get("fqdn", None),
    }
    return post
