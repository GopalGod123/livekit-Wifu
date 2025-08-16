# Meera Health Agent Backend (Flask + LiveKit)

A Flask token server plus a LiveKit Realtime Agent. The server issues JWTs for the frontend to join a LiveKit room and can start/stop a per-user agent process.

## Requirements
- Python 3.12+
- LiveKit Cloud project (URL, API Key, API Secret)
- Google API key for the Realtime model

## Environment
Create a `.env` file in `backend/`:
```
LIVEKIT_URL=wss://<your-subdomain>.livekit.cloud
LIVEKIT_API_KEY=lk_...
LIVEKIT_API_SECRET=...
GOOGLE_API_KEY=...
# Optional
PORT=8000
AGENT_PORT=9000
ROOM_NAME=meera-health-room
PARTICIPANT_IDENTITY=User
```

## Local run
```
python -m venv venv
# Windows PowerShell
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
python token_server.py
```
Health check: GET http://localhost:8000/health

## API
- POST `/get-token`
  - body: `{ "userName": string, "roomName": string }`
  - returns: `{ token, url }`
- POST `/agent/start` `{ userName, roomName }`
- POST `/agent/stop` `{ userName, roomName }`

## Run agent manually
```
python agent.py connect --room "<room>" --participant-identity "<name>"
```

## Docker
```
docker build -t livekit-backend .
docker run --rm -p 8000:8000 --env-file .env --name livekit-backend livekit-backend
```
Or with Compose (edit `.env` first):
```
docker compose up -d
```

## Deploy
- Image exposes `PORT` (default 8000) and `/health` for health checks.
- Set env vars on your host: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `GOOGLE_API_KEY`.
- Optional: `AGENT_PORT`, `ROOM_NAME`, `PARTICIPANT_IDENTITY`.

## Files
- `token_server.py`: Flask server, token + agent control
- `agent.py`: LiveKit Realtime agent (Google model, VAD, noise cancellation)
