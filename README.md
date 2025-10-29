# insta_pin_api

Instagram + Pinterest downloader API (private). Designed to be deployed on Render as a Web Service.

## How to deploy (summary)
1. Push this repo to a private GitHub repository.
2. On Render: New -> Web Service -> Connect GitHub -> choose this repo.
3. Set the Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. In Render Dashboard -> Environment -> Add `API_TOKEN` = your_secret_value.
5. Deploy.

## Usage
Send GET request to `/download?url=...` with header `x-api-key: <your_token>`.

Response example:
```json
{
  "status": "ok",
  "platform": "instagram",
  "media": [
    {"type":"image","url":"..."},
    {"type":"video","url":"..."}
  ]
}
```
