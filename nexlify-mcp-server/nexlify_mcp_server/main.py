from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging
import os

# Initialize FastMCP server
mcp = FastMCP(name = "Nexlify MCP Server", version = "0.1.3")
logging.basicConfig(level=logging.INFO)

# Constants
USER_AGENT = "nexlify_mcp_server/1.0"
NEXLIFY_API_BASE_URI = os.environ.get("NEXLIFY_API_BASE_URI", "http://0.0.0.0:8000")
MCP_TIMEOUT = os.environ.get("MCP_TIMEOUT", "500") # 500 seconds


DEFAULT_ERROR_MESSAGE = "Sorry, we couldn't process your request to the Nexlify API server at this time. Please try again later."

@mcp.tool(name = "nexlify_search", description="Search confluence pages using the Nexlify API")
def nexlify_search(query: str) -> str:
    """    Search confluence pages using the Nexlify API.
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