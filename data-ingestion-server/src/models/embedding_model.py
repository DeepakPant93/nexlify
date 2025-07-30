from typing import List, Optional
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]

# -----------  Input/Output Models ------------------


class SemanticSearchRequest(BaseModel):
    query: str
    collection: str = "dev_docs"
    top_k: int = 5
    filter_source: Optional[str] = None
    filter_filename: Optional[str] = None


class SearchResult(BaseModel):
    text: str
    score: float
    filename: Optional[str] = None
    title: Optional[str] = None
    chunk_index: Optional[int] = None
    source: Optional[str] = None


class SemanticSearchResponse(BaseModel):
    query: str
    collection: str
    results: List[SearchResult]
