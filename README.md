<div align="center">

# ⚡ Social Media Downloader REST API

<p align="center">
  <strong>High-performance, lightweight RESTful microservice built with Python and Flask for extracting direct media streams from Instagram and Pinterest posts.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Flask-REST_API-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Gunicorn-WSGI-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn" />
  <img src="https://img.shields.io/badge/Deployable-Render%20%7C%20Railway%20%7C%20VPS-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Deploy" />
</p>

[📖 API Documentation](#-api-documentation) • [🔒 Authentication](#-authentication) • [🚀 Quick Start](#-quick-start) • [🚢 Deployment](#-deployment)

</div>

---

## 📖 Overview

This repository provides a dedicated backend extraction API serving client applications such as Telegram bots (e.g. [@Ilyasov09/deku](https://github.com/Ilyasov09/deku)), web downloaders, or automation scripts. It resolves content URLs from **Instagram** (reels, photos, carousels) and **Pinterest** (pins, video pins) into direct, downloadable media links.

### ✨ Key Features

- **🎯 Unified Endpoint:** A single `/download` endpoint handles multi-platform URL parsing automatically.
- **🔐 Flexible Security:** Supports token authentication via standard `Authorization: Bearer <token>` or custom `x-api-key` headers.
- **⚡ Lightweight Footprint:** Built on Flask and WSGI (Gunicorn), minimizing memory footprint for cloud container deployments.
- **🛡️ Error Resilience:** Standardized JSON error structures with descriptive HTTP status codes.

---

## 📖 API Documentation

### 1. Health Check

Verifies server status and keeps container instances warm.

```http
GET /
```

#### Response (`200 OK`):
```json
{
  "status": "running ✅"
}
```

---

### 2. Extract Media

Resolves a public Instagram or Pinterest link into media objects.

```http
GET /download?url={target_url}
```

#### Parameters:

| Parameter | Type | In | Required | Description |
| :--- | :---: | :---: | :---: | :--- |
| `url` | string | query | **Yes** | Fully qualified URL from `instagram.com` or `pinterest.com` / `pin.it`. |

#### Response (`200 OK`):
```json
{
  "status": "ok",
  "platform": "instagram",
  "media": [
    {
      "type": "video",
      "url": "https://..."
    }
  ]
}
```

#### Error Responses:
- `400 Bad Request`: Missing query parameter or unsupported domain.
- `401 Unauthorized`: Invalid or missing authorization credentials.
- `500 Internal Server Error`: Extraction failure or target post is private.

---

## 🔒 Authentication

If the `API_KEY` environment variable is defined on the server, requests must include either of the following headers:

```http
Authorization: Bearer YOUR_SECRET_API_KEY
```
*or*
```http
x-api-key: YOUR_SECRET_API_KEY
```

*(If `API_KEY` is omitted from server environment, endpoints accept unauthenticated requests for local testing).*

---

## 💻 Code Examples

### cURL
```bash
curl -X GET "http://localhost:10000/download?url=https://www.instagram.com/reel/EXAMPLE/" \
     -H "x-api-key: your_secret_key"
```

### Python (`requests`)
```python
import requests

API_ENDPOINT = "https://your-api.onrender.com/download"
headers = {"x-api-key": "your_secret_key"}
params = {"url": "https://www.instagram.com/reel/EXAMPLE/"}

response = requests.get(API_ENDPOINT, headers=headers, params=params)
data = response.json()
print(data)
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Ilyasov09/api.git
cd api
```

### 2. Environment setup

```bash
python -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run server

```bash
# Development server
python main.py

# Production WSGI server
gunicorn main:app --bind 0.0.0.0:10000
```

---

## 🚢 Deployment

The repository includes a pre-configured `Procfile` for containerized hosting:

```
web: gunicorn main:app --bind 0.0.0.0:$PORT
```

### Deploying to Render / Railway:
1. Connect your GitHub repository `Ilyasov09/api`.
2. Select **Python** runtime environment.
3. Configure build & start commands:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app --bind 0.0.0.0:$PORT`
4. *(Optional)* Add `API_KEY` under Environment Variables.
5. Deploy.

---

## 📬 Author & Links

- **Developer:** Javlon Ilyasov
- **Telegram:** [@ilyasov09](https://t.me/ilyasov09)
- **GitHub:** [@Ilyasov09](https://github.com/Ilyasov09)
- **Channel:** [@cyberdevuz](https://t.me/cyberdevuz)

---

<div align="center">
  <sub>© 2026 Javlon Ilyasov. Lightweight media extraction backend.</sub>
</div>
