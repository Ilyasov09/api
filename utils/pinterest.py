import requests, re

def get_pinterest_media(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Agar short link (pin.it) bo‘lsa, redirect qilamiz
    if "pin.it" in url:
        try:
            r = requests.get(url, headers=headers, allow_redirects=True)
            url = r.url
        except:
            return None

    try:
        r = requests.get(url, headers=headers)
        html = r.text
    except:
        return None

    # 🔹 Video
    video_match = re.search(r'"contentUrl":"(https:[^"]+mp4)"', html)
    if video_match:
        video_url = video_match.group(1).replace("\\u0026", "&")
        return {
            "status": "ok",
            "platform": "pinterest",
            "media": [{"type": "video", "url": video_url}]
        }

    # 🔹 Rasm
    image_match = re.search(r'"image":"(https:[^"]+)"', html)
    if image_match:
        image_url = image_match.group(1).replace("\\u0026", "&")
        return {
            "status": "ok",
            "platform": "pinterest",
            "media": [{"type": "image", "url": image_url}]
        }

    return None
