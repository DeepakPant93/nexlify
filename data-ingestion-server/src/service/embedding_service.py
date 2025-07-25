import time
import logging
from typing import List, Optional
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, GoogleAPIError

logger = logging.getLogger("embedding_service")
logger.setLevel(logging.INFO)

MAX_RETRIES = 3
RETRY_BACKOFF = [2, 4, 8]  # in seconds


class GeminiEmbedder:
    def __init__(self, model_name: str = "models/embedding-001", task_type: str = "RETRIEVAL_DOCUMENT"):
        self.model_name = model_name
        self.task_type = task_type

    def get_embedding(self, text: str, title: Optional[str] = "Document Chunk") -> List[float]:
        for attempt in range(MAX_RETRIES):
            try:
                response = genai.embed_content(
                    model=self.model_name,
                    content=text,
                    task_type=self.task_type,
                    title=title
                )

                if hasattr(response, "embedding"):
                    return response.embedding
                elif isinstance(response, dict) and "embedding" in response:
                    return response["embedding"]
                else:
                    raise ValueError(
                        "No 'embedding' field in Gemini response.")

            except (ResourceExhausted, ServiceUnavailable) as retryable:
                wait_time = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF)-1)]
                logger.warning(
                    f"[Gemini] Retryable error on attempt {attempt+1}: {retryable}. Retrying in {wait_time}s.")
                time.sleep(wait_time)

            except GoogleAPIError as gerr:
                logger.error(f"[Gemini] API error: {gerr}")
                raise

            except Exception as e:
                logger.exception(f"[Gemini] Unexpected error: {e}")
                raise

        raise RuntimeError(
            "All Gemini embedding attempts failed after retries.")
