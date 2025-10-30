from flask import Flask, request, jsonify
from utils.instagram import get_instagram_media
from utils.pinterest import get_pinterest_media

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "running ✅",
        "message": "Universal Downloader API (Instagram + Pinterest)"
    })


@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL not provided"}), 400

    # Pinterest linkmi?
    if "pin.it" in url or "pinterest.com" in url:
        try:
            data = get_pinterest_media(url)
            if data:
                return jsonify(data)
            else:
                return jsonify({"error": "Pinterest media not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Instagram uchun
    elif "instagram.com" in url:
        try:
            data = get_instagram_media(url)
            if data:
                return jsonify(data)
            else:
                return jsonify({"error": "Instagram media not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        return jsonify({"error": "Unsupported platform"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
