import requests, re

def get_instagram_media(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text
    except Exception as e:
        return {"error": f"Failed to fetch page: {str(e)}"}

    # 🔹 Video URL
    video_match = re.search(r'"video_url":"(https:[^"]+)"', html)
    if video_match:
        video_url = video_match.group(1).replace("\\u0026", "&")
        return {
            "status": "ok",
            "platform": "instagram",
            "media": [{"type": "video", "url": video_url}]
        }

    # 🔹 Rasm URL
    image_match = re.search(r'"display_url":"(https:[^"]+)"', html)
    if image_match:
        image_url = image_match.group(1).replace("\\u0026", "&")
        return {
            "status": "ok",
            "platform": "instagram",
            "media": [{"type": "image", "url": image_url}]
        }

    return None
