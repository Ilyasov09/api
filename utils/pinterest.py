"""
Pinterest Media Extractor
Resolves public Pinterest pin URLs and returns direct video or image streams.
"""

import requests

def download_pinterest(url):
    try:
        api = "https://pinterestvideodownloader.io/api/"
        res = requests.get(api, params={"url": url}, timeout=20)
        data = res.json()

        if "video" in data:
            return {
                "status": "ok",
                "platform": "pinterest",
                "media": [{"type": "video", "url": data["video"]}]
            }
        elif "image" in data:
            return {
                "status": "ok",
                "platform": "pinterest",
                "media": [{"type": "image", "url": data["image"]}]
            }
        else:
            return {"status": "error", "detail": "No media found or pin is inaccessible"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
