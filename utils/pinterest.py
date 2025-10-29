import httpx
from bs4 import BeautifulSoup
from typing import Dict

async def get_pinterest_media(url: str) -> Dict:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        async with httpx.AsyncClient(timeout=15.0, headers=headers, follow_redirects=True) as client:
            r = await client.get(url)
            r.raise_for_status()
            html = r.text
    except Exception as e:
        return {"status": "error", "detail": f"Request failed: {str(e)}"}

    soup = BeautifulSoup(html, "html.parser")

    # Try og:video then og:image
    og_video = soup.find("meta", property="og:video")
    if og_video and og_video.get("content"):
        return {"status": "ok", "platform": "pinterest", "media": [{"type": "video", "url": og_video["content"]}]}

    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        return {"status": "ok", "platform": "pinterest", "media": [{"type": "image", "url": og_image["content"]}]}

    return {"status": "error", "detail": "No media found or post may be private."}
