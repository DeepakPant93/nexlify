from typing import List
from fastapi import APIRouter, Depends, File, HTTPException
from uuid import uuid4
import logging
from fastapi import UploadFile
from pydantic import BaseModel
from utils.ingest_util import extract_text_from_file
from fastapi import APIRouter, Depends, HTTPException, status
from core.ingest_controller import fetch_and_ingest_confluence_pages, get_embedding, ingest_file_to_qdrant
from models.embedding_model import EmbeddingRequest, EmbeddingResponse

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
