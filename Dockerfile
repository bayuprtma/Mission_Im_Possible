FROM python:3.11-slim

WORKDIR /app

# System deps (opsional, minimal dulu)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install missionimpossible (assuming published on PyPI)
RUN pip install --upgrade pip && pip install missionimpossible

# Default command: show help
CMD ["missionimpossible", "--help"]
