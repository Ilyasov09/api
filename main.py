from flask import Flask, request, jsonify
from auth import check_auth
from utils.instagram import download_instagram
from utils.pinterest import download_pinterest

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "running ✅"})

@app.route("/download")
def download():
    auth_error = check_auth()
    if auth_error:
        return auth_error

    url = request.args.get("url")
    if not url:
        return jsonify({"detail": "URL required"}), 400

    if "instagram.com" in url:
        return jsonify(download_instagram(url))
    elif "pin.it" in url or "pinterest.com" in url:
        return jsonify(download_pinterest(url))
    else:
        return jsonify({"detail": "Unsupported URL"}), 400
