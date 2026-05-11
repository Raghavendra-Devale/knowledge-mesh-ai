from pydantic import BaseModel
from typing import Any


class RetrievalResult(BaseModel):
    chunk_id: int
    content: str
    similarity_score: float | None = None
    metadata: dict[str, Any]
    retrieval_source: str = "semantic"


class RetrievalResponse(BaseModel):
    query: str
    results: list[RetrievalResult]