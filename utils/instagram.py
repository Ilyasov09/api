import requests, re

def download_instagram(url):
    try:
        api = "https://igram.world/api/ig/media"
        res = requests.post(api, json={"url": url})
        data = res.json()

        if "data" in data and len(data["data"]) > 0:
            media = []
            for item in data["data"]:
                media.append({
                    "type": "video" if ".mp4" in item["url"] else "image",
                    "url": item["url"]
                })
            return {"status": "ok", "platform": "instagram", "media": media}
        else:
            return {"status": "error", "detail": "No media found"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
