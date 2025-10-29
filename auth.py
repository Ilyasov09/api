import os
from fastapi import HTTPException, Header

# API_TOKEN must be set in Render environment variables (or your CI)
API_TOKEN = os.getenv("API_TOKEN")

def verify_token(x_api_key: str = Header(None)):
    if not API_TOKEN:
        raise HTTPException(status_code=500, detail="Server misconfiguration: API_TOKEN not set.")
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
