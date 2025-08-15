FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for audio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libffi-dev \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

# Health check endpoint for Render style monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:${PORT}/health || exit 1

# Run both: agent (background) + web (foreground). Render sends $PORT for web.
# Configure via env:
# - ROOM_NAME (default: meera-health-room)
# - PARTICIPANT_IDENTITY (default: User)
# - AGENT_PORT (default: 9000) to avoid conflict with web $PORT
# - GOOGLE_API_KEY, LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET must be set
CMD ["sh", "-c", "PORT=${AGENT_PORT:-9000} python -u agent.py connect --room \"${ROOM_NAME:-meera-health-room}\" --participant-identity \"${PARTICIPANT_IDENTITY:-User}\" & exec gunicorn -b 0.0.0.0:${PORT:-8000} token_server:app"]
