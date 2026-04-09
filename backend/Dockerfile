FROM python:3.12-slim

# python:3.12-slim (not alpine) — alpine lacks the C build tools required
# by chromadb's native dependencies (hnswlib, grpcio)

WORKDIR /app

# Install dependencies before copying source code so Docker can cache this layer.
# If only source code changes, the pip install layer is not rebuilt.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source
COPY . .

# The server runs on port 8000
EXPOSE 8000

# Ingest is run separately as a one-shot step before starting the server.
# See docker-compose.yml for the ingest service definition.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
