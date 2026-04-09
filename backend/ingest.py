"""
CLI script — run this once before starting the server.

Usage:
    python ingest.py

This script loads all PDFs from the data/pdfs/ directory, splits them into chunks,
embeds them using OpenAI, and stores the results in a local Chroma vector database.

Re-running this script on a database that already exists will add duplicate chunks.
To start fresh, delete the chroma_db/ directory before re-running.
"""

from app.services.ingestion_pipeline import run_ingestion_pipeline

if __name__ == "__main__":
    run_ingestion_pipeline()
