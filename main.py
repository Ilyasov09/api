from flask import Flask, request, jsonify
from auth import check_auth
from utils.instagram import download_instagram
from utils.pinterest import download_pinterest

# Flask app yaratamiz
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "API running ✅"})

@app.route("/download", methods=["GET"])
def download():
    # Autentifikatsiyani tekshiramiz
    auth_error = check_auth()
    if auth_error:
        return auth_error

    url = request.args.get("url")
    if not url:
        return jsonify({"detail": "URL required"}), 400

    try:
        if "instagram.com" in url:
            data = download_instagram(url)
        elif "pin.it" in url or "pinterest.com" in url:
            data = download_pinterest(url)
        else:
            return jsonify({"detail": "Unsupported URL"}), 400

        return jsonify(data)
    except Exception as e:
        # Xatolikni qaytaramiz
        return jsonify({"detail": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    # Local test uchun
    app.run(host="0.0.0.0", port=10000)
