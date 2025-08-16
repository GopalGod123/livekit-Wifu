# Meera Health Companion Frontend (React + Vite + LiveKit)

A React app using `@livekit/components-react` to join a LiveKit room and talk to the Meera health agent.

## Requirements
- Node.js 18+

## Environment
Set the backend token server URL for local/dev or production:
```
VITE_TOKEN_SERVER=http://localhost:8000
# or your deployed backend URL, e.g.
# VITE_TOKEN_SERVER=https://<your-backend>.onrender.com
```

## Scripts
- `npm run dev` — start Vite dev server
- `npm run build` — build for production
- `npm run preview` — preview production build

## Run locally
```
npm install
npm run dev
```
Then open the printed URL (usually http://localhost:5173). Ensure the backend is running and reachable at `VITE_TOKEN_SERVER`.

## How it connects
The app calls your backend:
- `POST /get-token` `{ userName, roomName }` → returns `{ token, url }`
- On connect/disconnect it also calls `/agent/start` and `/agent/stop` for on-demand agent control.

## Deploy
- Static deploy (Vercel/Netlify/etc.) works out of the box.
- Set `VITE_TOKEN_SERVER` in your hosting environment to your deployed backend, e.g. `https://<your-backend>.onrender.com`.

## Notes
- Uses `@livekit/components-react` with `@livekit/components-styles`.
- Built with Vite and React 19.
