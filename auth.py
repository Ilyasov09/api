import os
from flask import request, jsonify

def check_auth():
    api_key = os.getenv("API_KEY")
    key = request.headers.get("Authorization")
    if not key or key != f"Bearer {api_key}":
        return jsonify({"detail": "Unauthorized"}), 401
    return None
