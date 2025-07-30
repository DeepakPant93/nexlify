import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from core.ingest_controller import get_embedding
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException
from uuid import uuid4
import logging
from fastapi import UploadFile
from pydantic import BaseModel
from utils.ingest_util import extract_text_from_file
from fastapi import APIRouter, Depends, HTTPException, status
from core.ingest_controller import fetch_and_ingest_confluence_pages, get_embedding, ingest_file_to_qdrant
from models.embedding_model import EmbeddingRequest, EmbeddingResponse, SearchResult, SemanticSearchRequest, SemanticSearchResponse

router = APIRouter()


@router.post("/admin/confluence")
def ingest_confluence_docs():
    fetch_and_ingest_confluence_pages()
    return {"status": "success", "source": "confluence"}



@router.post("/admin/docs")
async def upload_dev_doc(
    file: UploadFile = File(...),
    collection: str = "dev_docs",
):
    try:
        # Extract text
        extracted_text = await extract_text_from_file(file)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400, detail="No extractable content found.")

        # Ingest to vector DB
        await ingest_file_to_qdrant(
            content=extracted_text,
            filename=file.filename,
            collection_name=collection
        )

        return {"status": "success", "message": f"Ingested {file.filename} into {collection}"}

    except Exception as e:
        logging.exception("Error while uploading developer documentation")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embeddings", response_model=EmbeddingResponse)
async def embed_text(request: EmbeddingRequest):
    """
    Generate embedding for a single text string using GeminiEmbedder.
    """
    try:
        embedding = get_embedding(request.text)
        return EmbeddingResponse(embedding=embedding)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", summary="Health check")
def health_check():
    return {"status": "ok"}


qdrant = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"),
                      port=int(os.getenv("QDRANT_PORT", 6333)))


@router.post("/search", response_model=SemanticSearchResponse)
async def semantic_search(req: SemanticSearchRequest):
    try:
        # 1. Embed query
        query_vector = get_embedding(req.query)

        # 2. Prepare filters (optional)
        filters = []
        if req.filter_source:
            filters.append(FieldCondition(
                key="source", match=MatchValue(value=req.filter_source)))
        if req.filter_filename:
            filters.append(FieldCondition(
                key="filename", match=MatchValue(value=req.filter_filename)))

        final_filter = Filter(must=filters) if filters else None

        # 3. Query Qdrant
        search_result = qdrant.search(
            collection_name=req.collection,
            query_vector=query_vector,
            limit=req.top_k,
            with_payload=True,
            score_threshold=None,
            query_filter=final_filter
        )

        # 4. Format response
        results = []
        for item in search_result:
            payload = item.payload or {}
            results.append(SearchResult(
                text=payload.get("text", ""),
                score=item.score,
                filename=payload.get("filename"),
                title=payload.get("title"),
                chunk_index=payload.get("chunk_index"),
                source=payload.get("source")
            ))

        return SemanticSearchResponse(
            query=req.query,
            collection=req.collection,
            results=results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")
