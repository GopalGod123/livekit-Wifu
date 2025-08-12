FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for audio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libffi-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

# ✅ Fixed: Use ENTRYPOINT + CMD pattern
ENTRYPOINT ["python", "agent.py"]
CMD ["start"]
