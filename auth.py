from fastapi import Header, HTTPException

TOKEN = "ppaallaakkaatt"  # o'zing tokenni bu yerga yoz

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
