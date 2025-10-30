import requests

def download_pinterest(url):
    try:
        api = "https://pinterestvideodownloader.io/api/"
        res = requests.get(api, params={"url": url})
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
            return {"status": "error", "detail": "No media found"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
