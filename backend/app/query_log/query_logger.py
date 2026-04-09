import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


# Anchored to this file's location so the path is correct regardless of
# which directory the server is started from.
DB_PATH = Path(__file__).parent.parent.parent / "logs" / "queries.db"

logger = logging.getLogger(__name__)


def initialize_database() -> None:
    """
    Creates the queries table if it does not already exist.
    Safe to call on every startup — does nothing if the table is already there.
    """
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp    TEXT    NOT NULL,
                question     TEXT    NOT NULL,
                answer       TEXT    NOT NULL,
                sources      TEXT    NOT NULL,
                latency_ms   INTEGER NOT NULL
            )
        """)


def log_query(
    question: str,
    answer: str,
    sources: list[dict],
    latency_ms: int,
) -> None:
    """
    Writes one query record to the SQLite log.
    Failures are caught and logged — a logging error must not kill a successful chat response.

    Args:
        question:   The user's original question.
        answer:     The LLM's generated answer.
        sources:    List of retrieved source document metadata dicts.
        latency_ms: Total time from request received to response sent, in milliseconds.
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute(
                """
                INSERT INTO queries (timestamp, question, answer, sources, latency_ms)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    question,
                    answer,
                    json.dumps(sources),
                    latency_ms,
                ),
            )
    except sqlite3.Error as error:
        logger.error("Failed to log query to SQLite: %s", error)
