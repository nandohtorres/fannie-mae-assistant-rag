FROM python:3.12-slim

# python:3.12-slim (not alpine) — alpine lacks the C build tools required
# by chromadb's native dependencies (hnswlib, grpcio)

WORKDIR /app

# Install C/C++ build tools required by chroma-hnswlib (a native extension).
# python:3.12-slim ships without gcc/g++ so we add them explicitly.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies before copying source code so Docker can cache this layer.
# If only source code changes, the pip install layer is not rebuilt.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# The server runs on port 8000
EXPOSE 8000

# start.sh checks if the Chroma DB is already populated (volume data persists
# across redeploys on Railway). If empty, it runs ingest first, then starts
# the server. This means ingest only runs once on a fresh volume.
CMD ["bash", "start.sh"]
