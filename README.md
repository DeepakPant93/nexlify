# Nexlify - A RAG-based AI chatbot integrated with GitHub Copilot

**A Retrieval-Augmented Generation (RAG) AI chatbot using CrewAI, FastAPI, and vector database integration**

## Overview

Nexlify is an AI-powered chatbot that enhances code development by integrating Retrieval-Augmented Generation (RAG) with GitHub Copilot. It processes data into a vector database, uses AI agents for querying internal documents and the internet, and connects to AI clients like GitHub Copilot or ChatGPT via the MCP server. Built with modern Python frameworks, it streamlines data ingestion, semantic search, and agentic workflows for developers.

This repository contains three projects:

1. [data-ingestion-server](./data-ingestion-server/README.md)
For data ingestion into the vector database.
2. [nexlify-ai-agentics-server](./nexlify-ai-agentics-server/README.md)
For the Agentic AI server, which queries the vector database using the data ingestion service and browses the internet.
3. [nexlify-mcp-server](./nexlify-mcp-server/README.md)
The MCP server to connect your AI client, such as GitHub Copilot or ChatGPT, to the AI server.

For more in-depth information on each component, please consult their individual README files located in the directories linked above. To explore Nexlify further, check out the [Nexlify Docs](docs/README.md).

## Features

- **RAG-based querying**: Retrieves and generates responses from vectorized data using embeddings and Qdrant database.
- **AI agent orchestration**: Employs CrewAI agents for parallel tasks like vector DB search and internet browsing.
- **Data ingestion**: Supports uploading and processing files (PDF, HTML, etc.) into a vector database with authentication.
- **Copilot integration**: MCP server enables seamless connection to GitHub Copilot for enhanced code assistance.
- **Scalable infrastructure**: Uses Docker for containerization, Terraform for AWS provisioning, and GitHub Actions for CI/CD.
- **Semantic search**: Performs efficient searches on whitelisted endpoints and internal data sources.


## Tech Stack

- **Python**: Core programming language.
- **FastAPI**: For building high-performance API microservices.
- **CrewAI**: Agent-based framework for task orchestration and automation.
- **Google Gemini**: For generating embeddings and LLM interactions.
- **Qdrant**: Vector database for storing and querying embeddings.
- **Docker**: Containerization for local and production deployment.
- **Terraform**: Infrastructure as code for AWS resources.
- **GitHub Actions**: CI/CD pipelines for automated builds and deployments.
- **Additional libraries**: PyPDF2 for PDF processing, Pandas for data manipulation, Pytest for testing.


## Backend Configuration

### Prerequisites

1. Install Docker and Docker Compose for local development.
2. Ensure Python 3.10+ is installed.
3. Clone the repository:

```bash
git clone https://github.com/DeepakPant93/nexlify.git
cd nexlify
```


### Running the Servers

To start the services locally using Docker Compose:

```bash
docker-compose up --build
```

- Data Ingestion service available at `http://localhost:7860`.
- AI Agentics service available at `http://localhost:8000`.


## Future Enhancements

- Support for additional file formats and data sources.
- Integration with more AI clients beyond Copilot and ChatGPT.
- Enhanced security features like advanced authentication and encryption.
- UI dashboard for monitoring and managing data ingestion.


## License

[MIT License](./LICENSE)

## Contributors

- Deepak Pant (@DeepakPant93)
- Dewasheesh Rana (@drana3)

## Acknowledgements

- CrewAI documentation for agent orchestration.
- Google Gemini and Qdrant for embedding and vector database technologies.
- Terraform and Docker communities for infrastructure tools.


## Contact

For any queries, reach out at [deepak.93p@gmail.com](mailto:deepak.93p@gmail.com).

## Support

If you like this project and want to support, give a ⭐ to the repo.

Thank you so much ❤️.

Project URL: https://github.com/DeepakPant93/nexlify
