import re
import httpx
from typing import List, Dict

_CLEAN_REPLACEMENTS = [('\\u0026', '&'), ('\\/', '/')]

def _clean_url(u: str) -> str:
    for a, b in _CLEAN_REPLACEMENTS:
        u = u.replace(a, b)
    return u

async def get_instagram_media(url: str) -> Dict:
    """Returns dict like:
    {
        "status": "ok",
        "platform": "instagram",
        "media": [ {"type":"image"/"video","url":"..."}, ... ]
    }
    Uses httpx async request and regex to extract display_url / video_url from page HTML.
    Handles carousel posts by gathering all matches and de-duping.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        async with httpx.AsyncClient(timeout=15.0, headers=headers, follow_redirects=True) as client:
            r = await client.get(url)
            r.raise_for_status()
            html = r.text
    except Exception as e:
        return {"status": "error", "detail": f"Request failed: {str(e)}"}

    media = []

    # video_url occurrences
    video_urls = re.findall(r'"video_url":"([^"]+)"', html)
    for v in video_urls:
        media.append({"type": "video", "url": _clean_url(v)})

    # display_url occurrences (images)
    image_urls = re.findall(r'"display_url":"([^"]+)"', html)
    for i in image_urls:
        media.append({"type": "image", "url": _clean_url(i)})

    # og:image fallback
    og_images = re.findall(r'<meta property="og:image" content="([^"]+)"', html)
    for o in og_images:
        media.append({"type": "image", "url": _clean_url(o)})

    # Deduplicate preserving order
    unique = []
    seen = set()
    for m in media:
        if m["url"] in seen:
            continue
        seen.add(m["url"])
        unique.append(m)

    if not unique:
        return {"status": "error", "detail": "No media found or post may be private."}

    return {"status": "ok", "platform": "instagram", "media": unique}
