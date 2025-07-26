# Nexlify MCP Server Package

## Overview

The Nexlify MCP Server is a lightweight Python package designed to integrate GitHub Copilot with the Nexlify AI system. It acts as a bridge, allowing developers to send queries from their IDE directly to the Nexlify API server—a CrewAI-based agentic AI service. This server executes queries against a vector database (powered by Qdrant) for internal documentation and performs restricted searches on whitelisted URLs (e.g., GitHub, StackOverflow) to retrieve relevant results. The package implements the Model Context Protocol (MCP) for seamless communication with GitHub Copilot, enhancing developer productivity by providing RAG-based (Retrieval-Augmented Generation) responses within the IDE.

Key features include:

- Simple query forwarding to the Nexlify CrewAI microservice.
- Support for semantic searches using embeddings stored in Qdrant.
- Restriction to whitelisted URLs for safe and targeted internet searches.
- Easy setup for local running and IDE integration.

This package is part of the Nexlify MVP, which leverages technologies like FastAPI, CrewAI, and Gemini AI for embedding generation.

## Installation

To install the latest version of the Nexlify MCP package, use pip. It is published on PyPI for easy access.

```bash
pip install nexlify-mcp-server
```


### Requirements

- Python 3.10 or higher.
- Dependencies: `requests` (automatically installed via pip).


## Configuration

Before using the package, configure your environment and IDE.

### Environment Variables

Create a `.env` file in your project root with the following (take reference from `.env.example`):

```
NEXLIFY_API_BASE_URI=<your_api_base_uri>
MCP_TIMEOUT=500 # Timeout in seconds
```

Load these variables using `python-dotenv` if needed in custom scripts.

### IDE Setup

- **VS Code**: Add the MCP server configuration to `.vscode/mcp.json` or `settings.json`. Enable MCP discovery with `"chat.mcp.discovery.enabled": true` and specify the local server URL (e.g., `http://localhost:8000`).
- **IntelliJ IDEA**: Configure via the Tools menu. Add the MCP server endpoint and enable integration for GitHub Copilot queries.

Ensure the Nexlify CrewAI microservice is running and accessible (e.g., via Docker Compose or AWS EC2 deployment).

Add this JSON configuration in your current workspace, file -> .vscode/mcp.json

```json
{
  "servers": {
    "nexlify-mcp-server": {
      "type": "stdio",
      "command": "nexlify_mcp_server",
      "env": {
        "NEXLIFY_API_BASE_URI": "${input:nexlify-app-uri}",
      }
      
    }
  },
  "inputs": [
    {
      "id": "nexlify-app-uri",
      "type": "promptString",
      "description": "Enter the URL of your Netlify app.",
      "default": "http://0.0.0.0:8000",
    },
  ],
}
```


## Usage

### Running the MCP Server

To run the MCP server, execute this command:

```bash
nexlify-mcp-server
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

## Publishing the Package

To publish the package, create a PyPI token using this URL: (https://pypi.org/manage/account/token/)

## Package Details

To check the package details, follow this link: (https://pypi.org/project/nexlify-mcp-server/)

## Make Commands

| Command | Description | Usage Example |
| :-- | :-- | :-- |
| run | Run the application | make run |
| build | Build the application | make build |
| install | Install the local build package (For Development only) | make install PYTHON_PATH="<your-python-path>" |
| publish | Publish the application | make publish |

## Limitations

- Relies on the availability of the Nexlify CrewAI microservice.
- Queries are limited to text-based inputs; no support for file uploads in MVP.
- Internet searches are restricted to whitelisted URLs for safety.


## License

This package is licensed under the [MIT License](../LICENSE). See the LICENSE file in the repository for details.
