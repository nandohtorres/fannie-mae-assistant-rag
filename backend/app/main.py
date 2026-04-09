import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.chains.rag_chain import build_rag_chain
from app.config import settings
from app.limiter import limiter
from app.query_log.query_logger import initialize_database
from app.routers import chat
from app.services.retriever import build_retriever
import app.state as app_state

logger = logging.getLogger(__name__)

INGEST_POLL_INTERVAL_SECONDS = 30


async def _poll_until_ready():
    """
    Background task that retries building the RAG chain every 30 seconds
    until the ingest pipeline finishes writing to the Chroma volume.
    """
    while True:
        await asyncio.sleep(INGEST_POLL_INTERVAL_SECONDS)
        try:
            retriever, document_count = build_retriever()
            if retriever is not None:
                app_state.rag_chain = build_rag_chain(retriever)
                app_state.document_count = document_count
                logger.info("RAG chain ready. %d document chunks indexed.", document_count)
                return
            logger.info("Ingest still running — will retry in %ds.", INGEST_POLL_INTERVAL_SECONDS)
        except Exception:
            logger.exception("Error while polling for Chroma readiness.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once when the server starts and once when it shuts down.
    If the Chroma DB is already populated (volume has data), builds the RAG chain immediately.
    If empty (ingest is running in the background via start.sh), starts polling until ready.
    """
    initialize_database()

    retriever, document_count = build_retriever()

    if retriever is not None:
        app_state.rag_chain = build_rag_chain(retriever)
        app_state.document_count = document_count
        logger.info("RAG chain ready. %d document chunks indexed.", document_count)
    else:
        logger.info("Chroma DB is empty — ingest is running in background. Polling every %ds.", INGEST_POLL_INTERVAL_SECONDS)
        asyncio.create_task(_poll_until_ready())

    yield


app = FastAPI(
    title="Fannie Mae RAG Assistant",
    description="A RAG-powered assistant grounded in Fannie Mae Selling and Servicing Guide documentation.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
