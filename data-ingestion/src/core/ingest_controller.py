from qdrant_client.models import PointStruct
import os
import logging
import requests
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from uuid import uuid4
from sentence_transformers import SentenceTransformer
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type

# --- Configuration ---
# e.g. "https://your-domain.atlassian.net/wiki"
CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")  # e.g. "DEVOPS"
CONFLUENCE_API_USER = os.getenv("CONFLUENCE_API_USER")  # email
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")  # api token
CONFLUENCE_COLLECTION = os.getenv("CONFLUENCE_COLLECTION", "confluence_docs")
DOC_COLLECTION = os.getenv("DOC_COLLECTION", "dev_docs")

# --- Qdrant + Embedding Setup ---
qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("confluence_ingest")

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

            # Clean and prepare text
            text_content = clean_html_text(html_content)
            full_text = f"{title}\n\n{text_content}"
            vector = model.encode(full_text).tolist()

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

        # Ensure Qdrant collection exists
        ensure_collection_exists(
            CONFLUENCE_COLLECTION, model.get_sentence_embedding_dimension())

        # Upsert to Qdrant
        qdrant.upsert(collection_name=CONFLUENCE_COLLECTION, points=points)
        total_uploaded += len(points)
        logger.info(
            f"Uploaded {len(points)} pages (Total: {total_uploaded})")

        if not data.get("_links", {}).get("next"):
            break

        start += limit

    logger.info("Finished Confluence ingestion.")

# --- HTML Cleaner ---


def clean_html_text(html: str) -> str:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n", strip=True)


# Load model and client once (production-friendly)
model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"),
                      port=int(os.getenv("QDRANT_PORT", 6333)))


def ensure_collection_exists(collection_name: str, vector_size: int = None):
    from qdrant_client.models import VectorParams, Distance

    try:
        collections = qdrant.get_collections().collections
        if collection_name not in [c.name for c in collections]:
            logging.info(f"Creating new Qdrant collection: {collection_name}")
            qdrant.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size or model.get_sentence_embedding_dimension(),
                    distance=Distance.COSINE
                )
            )
    except Exception as e:
        logging.exception("Failed to ensure Qdrant collection")
        raise


async def ingest_file_to_qdrant(content: str, filename: str, collection_name: str):
    try:
        # Step 1: Ensure collection exists
        ensure_collection_exists(collection_name)

        # Step 2: Break into overlapping chunks
        chunk_size = 512
        overlap = 64
        chunks = []
        words = content.split()
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += chunk_size - overlap

        logging.info(f"Split content into {len(chunks)} chunks")

        # Step 3: Encode and prepare points
        vectors = model.encode(chunks).tolist()

        points = [
            PointStruct(
                id=str(uuid4()),
                vector=vec,
                payload={
                    "filename": filename,
                    "chunk_index": idx,
                    "text": chunk,
                    "source": "developer_upload"
                }
            )
            for idx, (chunk, vec) in enumerate(zip(chunks, vectors))
        ]

        # Step 4: Upsert to Qdrant
        qdrant.upsert(
            collection_name=collection_name,
            points=points
        )

        logging.info(
            f"Successfully ingested {len(points)} chunks from {filename} into {collection_name}")

    except Exception as e:
        logging.exception(
            f"Failed to ingest file {filename} into {collection_name}")
        raise
