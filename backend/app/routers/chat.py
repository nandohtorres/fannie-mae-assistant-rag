import os
import time

from fastapi import APIRouter, Depends, HTTPException, Request
from langchain_core.runnables import Runnable
from openai import OpenAIError

from app.limiter import limiter
from app.query_log.query_logger import log_query
from app.models.schemas import ChatRequest, ChatResponse, HealthResponse, SourceDocument
import app.state as app_state


router = APIRouter(prefix="/api")


def get_rag_chain() -> Runnable:
    """
    FastAPI dependency that returns the shared RAG chain.
    The chain is initialized once at startup in main.py lifespan.
    Raises HTTP 503 if the chain has not loaded yet.
    """
    if app_state.rag_chain is None:
        raise HTTPException(
            status_code=503,
            detail="The knowledge base is still loading. Please try again in a few minutes.",
        )
    return app_state.rag_chain


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(request: Request, body: ChatRequest, chain: Runnable = Depends(get_rag_chain)) -> ChatResponse:
    """
    Accepts a user question, retrieves relevant document chunks from Chroma,
    passes them to the LLM, and returns an answer with source citations.
    """
    start_time = time.monotonic()

    try:
        result = await chain.ainvoke({"input": body.message})
    except OpenAIError as error:
        raise HTTPException(
            status_code=502,
            detail="Upstream AI service error. Please try again.",
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Internal error. Please try again.",
        ) from error

    latency_ms = int((time.monotonic() - start_time) * 1000)

    sources = [
        SourceDocument(
            source_file=os.path.basename(doc.metadata.get("source", "unknown")),
            # PyPDFLoader uses 0-based page numbers; add 1 for human-readable display.
            page_number=doc.metadata.get("page") + 1 if doc.metadata.get("page") is not None else None,
            excerpt=doc.page_content[:200],
        )
        for doc in result["context"]
    ]

    sources_as_dicts = [source.model_dump() for source in sources]
    log_query(
        question=body.message,
        answer=result["answer"],
        sources=sources_as_dicts,
        latency_ms=latency_ms,
    )

    return ChatResponse(answer=result["answer"], sources=sources)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Returns the current health status of the API.
    Checks whether the RAG chain is loaded and how many documents are indexed.
    """
    if app_state.rag_chain is None:
        return HealthResponse(status="loading", documents_indexed=0)

    document_count = app_state.document_count
    return HealthResponse(status="ok", documents_indexed=document_count)
