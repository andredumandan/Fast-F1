# Deploying the FastF1 Live Service

## 1️⃣ Build the container
```
cd fastf1-service
docker build -t fastf1-service .
``` 
(If you don’t have Docker locally, just push this folder to a repository and let Render build it.)

## 2️⃣ Create a **Background Worker** on Render
1. Sign in to <https://render.com>.
2. Click **New** → **Background Worker**.
3. Point the worker to your GitHub repo that contains the `fastf1-service` folder.
4. Render will automatically detect the Dockerfile and build the image.
5. In the *Environment* section add a key:
   - `FASTF1_URL = https://<worker>.onrender.com`
6. Save and let Render start the worker.

## 3️⃣ Connect your Next.js app to the worker
Add the following line to your Vercel project’s environment variables (or in `.env.local` for local dev):
```
FASTF1_URL=https://<worker>.onrender.com
```
Your `pages/api/live.ts` will proxy requests to this URL.

## 4️⃣ Verify the service
After the worker is running, visit:
```
https://<worker>.onrender.com/live?season=2026&round=12
```
You should receive a JSON array with telemetry for each driver. If you see an empty array or `503`, check that the SignalR client can connect to the official F1 feed.

## 5️⃣ Local Development (optional)
For local debugging you can run the FastAPI server directly:
```
pip install -r fastf1-service/requirements.txt
uvicorn fastf1-service.main:app --reload
```
Then set `FASTF1_URL=http://localhost:8000` in your `.env.local`.

---
**Note:** The FastF1 library requires an active internet connection to the official F1 telemetry endpoint. If you encounter rate limits or connectivity issues, consider adding a retry/backoff logic inside the SignalR worker.
