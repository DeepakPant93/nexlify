# Nexlify Data Ingestion Server & Search API

This project provides a production-ready FastAPI service to perform:

- File Upload & Text Extraction (PDF, HTML, etc.)
- Google Gemini Embedding with retry, backoff, and logging
- Qdrant Vector DB Ingestion with metadata
- Semantic Search with optional filters (filename, source)
- Confluence Page Crawler & Ingestor (with HTML cleanup)
- `/health` endpoint for health checks

> Designed with extensibility, observability, and deployment readiness in mind.


##  Tech Stack

- FastAPI – blazing fast API framework
- Qdrant – scalable vector database
- Gemini Embedding – Google Generative AI for vectorization
- OCR – Image-based PDF fallback with Tesseract
- Docker – containerized deployment
- Retry – robust error handling via `tenacity`

### 2. Set Environment Variables

Create a `.env` file or export these manually:

```env
QDRANT_HOST=localhost
QDRANT_PORT=6333

GEMINI_API_KEY=your_gemini_api_key

# Confluence Settings (optional)
CONFLUENCE_BASE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_SPACE_KEY=YOUR_SPACE
CONFLUENCE_API_USER=email@example.com
CONFLUENCE_API_TOKEN=your_token
```

---

## 🧪 Run Locally

```bash
uvicorn src.main:app --reload --port 7860
```

---

## 🚀 Docker

### Build & Run:

```bash
docker build -t ingest-api .
docker run -p 7860:7860 --env-file .env ingest-api
```

Ensure Qdrant is also running via Docker or cloud.

---

## 🔍 API Endpoints

### 📥 Upload File

`POST /admin/docs`

Upload a document (PDF, HTML, TXT) and ingest its content into Qdrant with metadata.

| Param       | Type     | Description            |
|-------------|----------|------------------------|
| file        | UploadFile | Document to upload    |
| collection  | string   | Qdrant collection name |

---

### 🧠 Semantic Search

`POST /search`

Performs semantic similarity search in Qdrant using Gemini embeddings.

```json
{
  "query": "How to integrate with OAuth?",
  "collection": "dev_docs",
  "top_k": 5,
  "filter_source": "developer_upload",
  "filter_filename": "auth_notes.pdf"
}
```

Returns `text`, `score`, `source`, and `filename` for each chunk.

---

### 🧾 Embed Text

`POST /embeddings`

```json
{
  "text": "This is a test paragraph"
}
```

Returns:

```json
{
  "embedding": [0.012, 0.32, ...]
}
```

---

### 🌐 Confluence Ingestion

`POST /admin/confluence`

Ingests all Confluence pages in a given space. Requires Confluence API creds.

---

### 🔄 Health Check

`GET /health`

Simple service status.

---

## 🧠 Models

### `EmbeddingRequest`
```json
{ "text": "string" }
```

### `SemanticSearchRequest`
```json
{
  "query": "string",
  "collection": "string",
  "top_k": 5,
  "filter_source": "string",
  "filter_filename": "string"
}
```

---

## 🛡️ Security Best Practices

- Strip all PII before storing in vector DB.
- Log embedding failures, but never content.
- Avoid embedding user input directly without validation.
- Optional: Secure endpoints using JWT (see FastAPI dependencies).
- Use Docker secrets or Vault for sensitive keys.

---

## 📈 Recommended Enhancements

- Add JWT auth for admin upload
- Stream search results via SSE
- Add hybrid search (keyword + vector)
- Async Gemini embedding pipeline
- Redis cache for frequent embeddings

---

## 🤝 Contributing

1. Fork this repo
2. Clone + branch out
3. Submit a PR with clear description
4. Include tests if possible



