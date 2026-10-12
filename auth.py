"""
Authentication middleware for API endpoints.
Validates requests using either standard Authorization Bearer tokens or x-api-key headers.
"""

import os
from flask import request, jsonify

def check_auth():
    api_key = os.getenv("API_KEY")
    # If no API key is enforced in environment, allow open access
    if not api_key:
        return None

    auth_header = request.headers.get("Authorization", "")
    x_api_key = request.headers.get("x-api-key", "")

    # Check both 'Authorization: Bearer <token>' and 'x-api-key: <token>'
    if auth_header == f"Bearer {api_key}" or x_api_key == api_key:
        return None

    return jsonify({"detail": "Unauthorized"}), 401
