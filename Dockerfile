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

# ✅ Added health check for Railway monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:${PORT}/health', timeout=5)" || exit 1

# Start Meera in production mode
ENTRYPOINT ["python", "agent.py"]
CMD ["start"]
