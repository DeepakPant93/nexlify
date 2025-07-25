from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging
import os

# Initialize FastMCP server
mcp = FastMCP("weather")
logging.basicConfig(level=logging.INFO)

# Constants
USER_AGENT = "nexlify_mcp_server/1.0"
NEXLIFY_API_BASE_URI = os.environ.get("NEXLIFY_API_BASE_URI", "http://0.0.0.0:8000")
MCP_TIMEOUT = os.environ.get("MCP_TIMEOUT", "500") # 500 seconds


DEFAULT_ERROR_MESSAGE = "Sorry, we couldn't process your request to the Netlify API server at this time. Please try again later."

@mcp.tool()
def nexlify_search(query: str) -> str:
    """    Search for a query using the Netlify API.
    Args:
        query (str): The search query.
    Returns:
        str: The search results.
    """
    res = httpx.post(f"{NEXLIFY_API_BASE_URI}/search", json={"query": query}, headers={"User-Agent": USER_AGENT}, timeout=int(MCP_TIMEOUT)).json()
    return res.get("response", DEFAULT_ERROR_MESSAGE)


def run() -> None:
    """Run the MCP server."""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    # Initialize and run the server
    logging.info("Starting Nexlify MCP server...")
    run()