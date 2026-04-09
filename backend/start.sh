#!/bin/bash

# Check if the Chroma vector store already has data.
COLLECTION_COUNT=$(python -c "
try:
    import chromadb
    client = chromadb.PersistentClient('./chroma_db')
    col = client.get_collection('fannie_mae_docs')
    print(col.count())
except Exception:
    print(0)
" 2>/dev/null || echo 0)

if [ "$COLLECTION_COUNT" -eq "0" ]; then
    echo "Chroma DB is empty — starting ingest in background..."
    python ingest.py &
else
    echo "Chroma DB has $COLLECTION_COUNT chunks — skipping ingest."
fi

# Start the server immediately regardless of ingest status.
# The server handles the not-ready state gracefully until ingest finishes.
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
