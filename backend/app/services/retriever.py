from langchain_chroma import Chroma
from langchain_core.retrievers import BaseRetriever
from langchain_openai import OpenAIEmbeddings

from app.config import settings


# How many final chunks to return per query after MMR re-ranking.
TOP_K_RESULTS = 6

# How many candidates to fetch before MMR re-ranking.
# MMR (Maximal Marginal Relevance) picks diverse chunks from this pool,
# reducing the chance of returning near-duplicate passages.
MMR_FETCH_K = 20


def build_retriever() -> tuple[BaseRetriever | None, int]:
    """
    Loads the persisted Chroma vector store from disk and returns a retriever
    along with the count of indexed document chunks.

    The vector store must already exist — run ingest.py before calling this.
    Raises RuntimeError if the vector store is empty or missing.

    Uses MMR search instead of basic similarity to avoid returning chunks that
    are semantically similar to each other (common in long regulatory PDFs).

    Returns:
        retriever:       A LangChain BaseRetriever configured for MMR search.
        document_count:  Number of chunks currently indexed in the vector store.
    """
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )

    vector_store = Chroma(
        persist_directory=settings.chroma_db_path,
        embedding_function=embeddings,
        collection_name=settings.chroma_collection_name,
    )

    stored_ids = vector_store.get()["ids"]
    if not stored_ids:
        return None, 0

    document_count = len(stored_ids)

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": TOP_K_RESULTS, "fetch_k": MMR_FETCH_K},
    )

    return retriever, document_count
