import os
from fastapi import FastAPI, Query, Depends
from fastapi.responses import JSONResponse
from auth import verify_token
from utils.instagram import get_instagram_media
from utils.pinterest import get_pinterest_media

app = FastAPI(title="insta_pin_api", version="1.0")

def detect_platform(url: str) -> str:
    u = url.lower()
    if "instagram.com" in u:
        return "instagram"
    if "pin.it" in u or "pinterest.com" in u:
        return "pinterest"
    return "unknown"

@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "message": "insta_pin_api up"}

@app.get("/download", dependencies=[Depends(verify_token)])
async def download(url: str = Query(..., description="Instagram or Pinterest post URL")):
    platform = detect_platform(url)

    if platform == "instagram":
        result = await get_instagram_media(url)
    elif platform == "pinterest":
        result = await get_pinterest_media(url)
    else:
        return JSONResponse(status_code=400, content={"status": "error", "detail": "Unsupported platform"})

    if not result:
        return JSONResponse(status_code=500, content={"status": "error", "detail": "No media found"})

    return JSONResponse(status_code=200, content=result)
