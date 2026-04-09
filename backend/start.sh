#!/bin/bash
set -e

# Check if the Chroma vector store already has data.
# If the collection is empty or missing, run the ingest pipeline first.
# With a Railway volume mounted at /app/chroma_db, ingest only runs once
# and persists across restarts and redeploys.
COLLECTION_COUNT=$(python -c "
import sys
try:
    import chromadb
    client = chromadb.PersistentClient('./chroma_db')
    col = client.get_collection('fannie_mae_docs')
    print(col.count())
except Exception:
    print(0)
" 2>/dev/null || echo 0)

if [ "$COLLECTION_COUNT" -eq "0" ]; then
    echo "Chroma DB is empty — running ingest pipeline..."
    python ingest.py
else
    echo "Chroma DB has $COLLECTION_COUNT chunks — skipping ingest."
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
