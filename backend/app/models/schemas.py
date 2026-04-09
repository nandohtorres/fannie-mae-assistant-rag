from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """The body of a POST /api/chat request."""

    message: str = Field(min_length=1, max_length=2000)


class SourceDocument(BaseModel):
    """A single document chunk retrieved from the vector database."""

    source_file: str
    page_number: int | None
    excerpt: str


class ChatResponse(BaseModel):
    """The body of a POST /api/chat response."""

    answer: str
    sources: list[SourceDocument]


class HealthResponse(BaseModel):
    """The body of a GET /api/health response."""

    status: str
    documents_indexed: int
