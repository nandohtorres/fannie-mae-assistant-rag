"""
Shared application state — holds objects that are initialized at startup
and need to be accessible across the app without circular imports.

FastAPI's lifespan context sets these values once at boot.
Route handlers read from here via the get_rag_chain() dependency in routers/chat.py.
"""

from langchain_core.runnables import Runnable

rag_chain: Runnable | None = None
document_count: int = 0
