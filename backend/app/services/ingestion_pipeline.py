import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


# How many characters per chunk. 1000 chars (~200 tokens) gives precise retrieval
# for dense regulatory text without losing too much context.
CHUNK_SIZE = 1000

# How many characters of overlap between adjacent chunks.
# Prevents a sentence split across a boundary from losing its meaning.
CHUNK_OVERLAP = 200


def load_pdf_documents(pdf_directory: str) -> list[Document]:
    """
    Loads all PDF files from the given directory.
    Returns a flat list of LangChain Document objects, one per page.
    Each Document carries metadata: source filename and page number.
    """
    all_documents: list[Document] = []

    for filename in os.listdir(pdf_directory):
        if not filename.endswith(".pdf"):
            continue

        file_path = os.path.join(pdf_directory, filename)
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        all_documents.extend(pages)
        print(f"Loaded {len(pages)} pages from {filename}")

    return all_documents


def split_documents_into_chunks(documents: list[Document]) -> list[Document]:
    """
    Splits the loaded documents into smaller chunks for embedding.
    Uses RecursiveCharacterTextSplitter which respects natural text boundaries
    (paragraphs, then sentences, then words) before splitting mid-word.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )
    chunks = splitter.split_documents(documents)
    print(f"Split {len(documents)} pages into {len(chunks)} chunks")
    return chunks


CHROMA_MAX_BATCH_SIZE = 5000


def embed_and_store_chunks(chunks: list[Document]) -> Chroma:
    """
    Embeds each chunk using the OpenAI embedding model and stores the results
    in a local Chroma vector database. The database persists to disk at the
    path defined in settings.chroma_db_path.

    Chroma has a max batch size of 5461 — chunks are added in batches of 5000
    to stay safely under that limit.

    Returns the populated Chroma vector store instance.
    """
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )

    first_batch = chunks[:CHROMA_MAX_BATCH_SIZE]
    vector_store = Chroma.from_documents(
        documents=first_batch,
        embedding=embeddings,
        persist_directory=settings.chroma_db_path,
        collection_name=settings.chroma_collection_name,
    )

    for i in range(CHROMA_MAX_BATCH_SIZE, len(chunks), CHROMA_MAX_BATCH_SIZE):
        batch = chunks[i:i + CHROMA_MAX_BATCH_SIZE]
        vector_store.add_documents(batch)
        print(f"Added batch {i // CHROMA_MAX_BATCH_SIZE + 1}: chunks {i}–{i + len(batch)}")

    print(f"Stored {len(chunks)} chunks in Chroma at '{settings.chroma_db_path}'")
    return vector_store


def run_ingestion_pipeline() -> None:
    """
    Full ingestion pipeline: load PDFs → split into chunks → embed → store in Chroma.
    Run this once before starting the server. Re-running will add duplicate chunks
    unless you delete the chroma_db directory first.
    """
    print(f"Starting ingestion from '{settings.pdf_directory}'...")

    documents = load_pdf_documents(settings.pdf_directory)

    if not documents:
        print("No PDF files found. Add PDFs to the data/pdfs/ directory and re-run.")
        return

    chunks = split_documents_into_chunks(documents)
    embed_and_store_chunks(chunks)

    print("Ingestion complete. You can now start the server.")
