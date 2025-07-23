# Nexlify MCP Server Package

## Overview

The Nexlify MCP Server is a lightweight Python package designed to integrate GitHub Copilot with the Nexlify AI system. It acts as a bridge, allowing developers to send queries from their IDE directly to the Nexlify API server—a CrewAI-based agentic AI service. This server executes queries against a vector database (powered by Qdrant) for internal documentation and performs restricted searches on whitelisted URLs (e.g., GitHub, StackOverflow) to retrieve relevant results. The package implements the Model Context Protocol (MCP) for seamless communication with GitHub Copilot, enhancing developer productivity by providing RAG-based (Retrieval-Augmented Generation) responses within the IDE[1].

Key features include:
- Simple query forwarding to the Nexlify CrewAI microservice.
- Support for semantic searches using embeddings stored in Qdrant.
- Restriction to whitelisted URLs for safe and targeted internet searches.
- Easy setup for local running and IDE integration.

This package is part of the Nexlify MVP, which leverages technologies like FastAPI, CrewAI, and OpenAI for embedding generation[1].

## Installation

To install the Nexlify MCP package, use pip. It is published on PyPI for easy access.

```bash
pip install nexlify-mcp-server
```

### Requirements
- Python 3.10 or higher.
- Dependencies: `requests` (automatically installed via pip).

## Configuration

Before using the package, configure your environment and IDE.

### Environment Variables
Create a `.env` file in your project root with the following:

```
CREW_AI_URL=http://nexlify-ai-agentics-server:8001  # URL of the CrewAI microservice /search endpoint
```

Load these variables using `python-dotenv` if needed in custom scripts.

### IDE Setup
- **VS Code**: Add the MCP server configuration to `.vscode/mcp.json` or `settings.json`. Enable MCP discovery with `"chat.mcp.discovery.enabled": true` and specify the local server URL (e.g., `http://localhost:8000`)[1].
- **IntelliJ IDEA**: Configure via the Tools menu. Add the MCP server endpoint and enable integration for GitHub Copilot queries[1].

Ensure the Nexlify CrewAI microservice is running and accessible (e.g., via Docker Compose or AWS EC2 deployment).

## Usage

### Running the MCP Server
Run the server locally to handle queries from GitHub Copilot:

```bash
python -m nexlify_mcp
```

This starts a lightweight server that listens for MCP requests and forwards them to the configured CrewAI URL.

### Querying from IDE
Once running and configured in your IDE:
1. Open GitHub Copilot chat in VS Code or IntelliJ.
2. Submit a query (e.g., "How do I fix this Python error?").
3. The MCP server forwards the query to the CrewAI microservice.
4. The CrewAI service:
   - Queries the vector database for internal results.
   - Searches whitelisted URLs for external insights.
5. Consolidated results are returned and displayed in the IDE.

## Limitations

- Relies on the availability of the Nexlify CrewAI microservice.
- Queries are limited to text-based inputs; no support for file uploads in MVP.
- Internet searches are restricted to whitelisted URLs for safety[1].

## License

This package is licensed under the MIT License. See the LICENSE file in the repository for details.