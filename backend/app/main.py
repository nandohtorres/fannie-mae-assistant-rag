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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once when the server starts, and once when it shuts down.
    Startup: initializes the SQLite log, builds the retriever, builds the RAG chain.
    Shutdown: nothing to clean up for now.
    """
    # Set up the query log database (creates the table if it doesn't exist)
    initialize_database()

    # Load the persisted Chroma vector store and build the retriever
    retriever, document_count = build_retriever()

    # Store the document count for the /health endpoint
    app_state.document_count = document_count

    # Build the full RAG chain and store it in shared state
    app_state.rag_chain = build_rag_chain(retriever)

    logger.info("RAG chain ready. %d document chunks indexed.", app_state.document_count)

    yield  # Server runs here

    # Cleanup on shutdown (nothing required for Chroma local)


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
