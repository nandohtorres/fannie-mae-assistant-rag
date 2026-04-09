# Fannie Mae Guide Assistant

A production-quality RAG (Retrieval-Augmented Generation) chatbot grounded in the Fannie Mae
Selling Guide and Servicing Guide. Ask questions in plain English — the assistant answers using
only the source documents, with citations showing exactly which page each answer came from.

Built as a reusable portfolio template. Swapping the PDF corpus, system prompt, and README
produces a version of this tool for any document-heavy domain.

---

## What It Does

- Answers questions about Fannie Mae loan eligibility, property requirements, and servicing guidelines
- Every response includes source citations — document name and page number
- Answers are grounded strictly in the ingested documents — no hallucinated policy
- Rate limited to 10 requests per minute per IP to protect OpenAI API costs

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | OpenAI `gpt-4o-mini` |
| Embeddings | OpenAI `text-embedding-3-small` |
| Orchestration | LangChain 0.3.x (LCEL) |
| Vector database | Chroma (local persistent) |
| Backend | Python 3.12, FastAPI, uvicorn |
| Frontend | React 18, Vite |
| UI components | Material UI (MUI) |
| Containerization | Docker + docker-compose |
| Query logging | SQLite |

---

## Architecture

```
frontend/           React + Vite chat UI
backend/
  app/
    chains/         RAG chain (LCEL) — prompt + retriever wired together
    services/       Retriever and ingestion pipeline
    routers/        FastAPI route handlers (thin — delegate to chains)
    models/         Pydantic schemas for request/response validation
    query_log/      SQLite logger — records every question, answer, and latency
    config.py       All settings via pydantic-settings — no bare os.getenv()
  ingest.py         One-shot CLI script — loads PDFs into Chroma
  data/pdfs/        Source PDF documents
  chroma_db/        Persisted vector store (gitignored)
```

**Key decisions:**
- Ingest is a one-shot script, never called by the server at runtime
- The RAG chain and retriever are built once at startup via FastAPI `lifespan` — not per request
- The backend never executes user-submitted input as code
- All secrets live in `.env`, never in source code

---

## Running Locally

### Prerequisites
- Python 3.12
- Node.js 18+
- An OpenAI API key with billing enabled

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt

cp .env.example .env
# Edit .env — add your OPENAI_API_KEY and set ALLOWED_ORIGINS=http://localhost:5173
```

**Ingest the PDFs (first time only):**
```bash
python ingest.py
```
This reads all PDFs from `backend/data/pdfs/`, splits them into chunks, embeds them with
OpenAI, and stores the result in `backend/chroma_db/`. Only needs to run again if the
PDF corpus changes.

**Start the API server:**
```bash
uvicorn app.main:app --reload --port 8000
```
Wait for the startup log before starting the frontend.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

---

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `ALLOWED_ORIGINS` | Comma-separated list of frontend origins (e.g. `http://localhost:5173`) |
| `DEBUG` | Set to `true` to enable `/docs` and `/redoc` Swagger UI (default: `false`) |

---

## Re-Theme Pattern

To adapt this for a different domain, change only three things:

| What | Where |
|---|---|
| PDF corpus | `backend/data/pdfs/` |
| System prompt | `backend/app/chains/rag_chain.py` → `SYSTEM_PROMPT` constant |
| README title, description, screenshots | `README.md` |

Everything else — the pipeline, API, UI, Docker setup, query logging — stays identical.
