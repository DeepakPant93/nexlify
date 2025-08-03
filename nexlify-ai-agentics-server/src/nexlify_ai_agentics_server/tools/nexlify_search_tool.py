from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
import httpx
import os
from dotenv import load_dotenv
import logging

load_dotenv()

NEXLIFY_DATA_INGESTION_SERVICE_BASE_URI = os.getenv("NEXLIFY_DATA_INGESTION_SERVICE_BASE_URI", "http://localhost:7860")  # Default to localhost if not set
MCP_TIMEOUT = os.getenv("MCP_TIMEOUT", "500")  # Default timeout of 500 milliseconds if not set
USER_AGENT = os.getenv("USER_AGENT", "NexlifySearchTool/1.0")
DEFAULT_ERROR_MESSAGE = "Please check the inputs and try again. If the issue persists, contact support."
NO_INFO_MESSAGE = "No information found for the given query."


class NexlifySearchToolInput(BaseModel):
    """Input schema for NexlifySearchTool."""
    query: str = Field(..., description="Search query for the Nexlify search engine.")

class NexlifySearchTool(BaseTool):
    name: str = "Nexlify Search Tool"
    description: str = (
        "This tool allows you to search for information using the Nexlify search engine. You can use this tool to search for information about any topic."
    )
    args_schema: Type[BaseModel] = NexlifySearchToolInput

    def _run(self, query: str) -> Any:
        # Implementation of the search functionality goes here
        return self.__nexlify_search(query)


    def __nexlify_search(self, query: str) -> list | str:
        """    Search confluence pages using the Nexlify API.
        Args:
            query (str): The search query.
        Returns:
            list | str: The search results.
        """
        search_results = NO_INFO_MESSAGE
        request_body = {"query": query, "top_k": 3}
        try:
            # Make a POST request to the Nexlify search API
            res = httpx.post(f"{NEXLIFY_DATA_INGESTION_SERVICE_BASE_URI}/search", json=request_body, headers={"User-Agent": USER_AGENT}, timeout=int(MCP_TIMEOUT)).json()
            if res.get("results") is not None:
                search_results = res["results"]
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            search_results = DEFAULT_ERROR_MESSAGE

        return search_results