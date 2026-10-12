"""
Social Media Downloader REST API
A lightweight Flask service providing unified media extraction endpoints
for Instagram and Pinterest posts.
"""

from flask import Flask, request, jsonify
from auth import check_auth
from utils.instagram import download_instagram
from utils.pinterest import download_pinterest

app = Flask(__name__)

# --- Health Check ---
@app.route("/")
def home():
    return jsonify({"status": "running ✅"})

# --- Media Extraction Endpoint ---
@app.route("/download", methods=["GET"])
def download():
    # Verify client authentication if API_KEY is configured
    auth_error = check_auth()
    if auth_error:
        return auth_error

    url = request.args.get("url")
    if not url:
        return jsonify({"detail": "Query parameter 'url' is required"}), 400

    try:
        if "instagram.com" in url:
            data = download_instagram(url)
        elif "pin.it" in url or "pinterest.com" in url:
            data = download_pinterest(url)
        else:
            return jsonify({"detail": "Unsupported URL. Must be Instagram or Pinterest."}), 400
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
