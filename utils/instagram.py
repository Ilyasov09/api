import re
import httpx
from typing import Dict

_CLEAN_REPLACEMENTS = [('\\u0026', '&'), ('\\/', '/')]

def _clean_url(u: str) -> str:
    for a, b in _CLEAN_REPLACEMENTS:
        u = u.replace(a, b)
    return u

async def get_instagram_media(url: str) -> Dict:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        async with httpx.AsyncClient(timeout=15.0, headers=headers, follow_redirects=True) as client:
            r = await client.get(url)
            r.raise_for_status()
            html = r.text
    except Exception as e:
        return {"status": "error", "detail": f"Request failed: {str(e)}"}

    media = []

    # Video priority
    video_urls = re.findall(r'"video_url":"([^"]+)"', html)
    for v in video_urls:
        media.append({"type": "video", "url": _clean_url(v)})

    if media:
        # deduplicate
        unique = []
        seen = set()
        for m in media:
            if m["url"] not in seen:
                seen.add(m["url"])
                unique.append(m)
        return {"status": "ok", "platform": "instagram", "media": unique}

    # Fallback: images
    image_urls = re.findall(r'"display_url":"([^"]+)"', html)
    for i in image_urls:
        media.append({"type": "image", "url": _clean_url(i)})

    og_images = re.findall(r'<meta property="og:image" content="([^"]+)"', html)
    for o in og_images:
        media.append({"type": "image", "url": _clean_url(o)})

    # deduplicate images
    unique = []
    seen = set()
    for m in media:
        if m["url"] not in seen:
            seen.add(m["url"])
            unique.append(m)

    if not unique:
        return {"status": "error", "detail": "No media found or post may be private."}

    return {"status": "ok", "platform": "instagram", "media": unique}
