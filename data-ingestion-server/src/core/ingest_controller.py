from typing import List
from qdrant_client.models import PointStruct, VectorParams, Distance
import os
import logging
import requests
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from uuid import uuid4
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import google.generativeai as genai
from ..service.embedding_service import GeminiEmbedder

# --- Configuration ---
CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")
CONFLUENCE_API_USER = os.getenv("CONFLUENCE_API_USER")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
CONFLUENCE_COLLECTION = os.getenv("CONFLUENCE_COLLECTION", "confluence_docs")
DOC_COLLECTION = os.getenv("DOC_COLLECTION", "dev_docs")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Qdrant Setup ---
qdrant = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"),
                      port=int(os.getenv("QDRANT_PORT", 6333)))

gemini_embedder = GeminiEmbedder()
# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("confluence_ingest")

# --- Gemini Embedding ---
genai.configure(api_key=GEMINI_API_KEY)



# --- Retryable GET ---


@retry(wait=wait_fixed(2), stop=stop_after_attempt(3), retry=retry_if_exception_type(requests.RequestException))
def confluence_get(url: str, params: dict = None) -> dict:
    full_url = f"{CONFLUENCE_BASE_URL}/rest/api/{url}"
    logger.debug(f"Fetching URL: {full_url}")
    response = requests.get(
        full_url,
        params=params,
        auth=(CONFLUENCE_API_USER, CONFLUENCE_API_TOKEN),
        headers={"Accept": "application/json"},
        timeout=10
    )
    response.raise_for_status()
    return response.json()

# --- Main Ingestion Logic ---


def fetch_and_ingest_confluence_pages():
    logger.info("Starting Confluence content ingestion...")
    start = 0
    limit = 25
    total_uploaded = 0

    ensure_collection_exists(CONFLUENCE_COLLECTION, 768)
    while True:
        params = {
            "spaceKey": CONFLUENCE_SPACE_KEY,
            "expand": "body.storage",
            "start": start,
            "limit": limit
        }

        data = confluence_get("content", params=params)
        results = data.get("results", [])

        if not results:
            break

        points: List[PointStruct] = []
        for page in results:
            page_id = page["id"]
            title = page["title"]
            html_content = page.get("body", {}).get(
                "storage", {}).get("value", "")
            if not html_content:
                logger.warning(
                    f"No content found for page {page_id} - {title}")
                continue

            text_content = clean_html_text(html_content)
            full_text = f"{title}\n\n{text_content}"
            vector = gemini_embedder.get_embedding(full_text)

            point = PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload={
                    "title": title,
                    "page_id": page_id,
                    "text": text_content,
                    "source": "confluence"
                }
            )
            points.append(point)

        qdrant.upsert(collection_name=CONFLUENCE_COLLECTION, points=points)
        total_uploaded += len(points)
        logger.info(f"Uploaded {len(points)} pages (Total: {total_uploaded})")

        if not data.get("_links", {}).get("next"):
            break

        start += limit

    logger.info("Finished Confluence ingestion.")

# --- HTML Cleaner ---


def clean_html_text(html: str) -> str:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n", strip=True)

# --- Collection Ensurer ---


def ensure_collection_exists(collection_name: str, dim: int = 384):
    try:
        collections = qdrant.get_collections().collections
        names = [col.name for col in collections]
        if collection_name not in names:
            qdrant.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=dim, distance=Distance.COSINE),
            )
    except Exception as e:
        raise RuntimeError(f"Failed to ensure Qdrant collection: {e}")

# --- Generic File Ingestion ---


async def ingest_file_to_qdrant(content: str, filename: str, collection_name: str):
    try:
        chunk_size = 512
        overlap = 64
        words = content.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += chunk_size - overlap

        logging.info(f"Split content into {len(chunks)} chunks")
        ensure_collection_exists(
            collection_name, 768)

        points = []
        for idx, chunk in enumerate(chunks):
            vector = gemini_embedder.get_embedding(chunk)
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload={
                        "filename": filename,
                        "chunk_index": idx,
                        "text": chunk,
                        "source": "developer_upload"
                    }
                )
            )

        qdrant.upsert(collection_name=collection_name, points=points)
        logging.info(
            f"Successfully ingested {len(points)} chunks from {filename} into {collection_name}")

    except Exception as e:
        logging.exception(
            f"Failed to ingest file {filename} into {collection_name}")
        raise


# Utility method to get embedding for a given text


def get_embedding(text: str) -> List[float]:
    try:
        # Use Gemini embedder (could expand with fallback logic here)
        vector = gemini_embedder.get_embedding(text)
        return vector
    except Exception as e:
        # Handle/embed fallback or error logging
        raise RuntimeError(f"Embedding generation failed: {e}")
