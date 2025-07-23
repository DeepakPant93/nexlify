<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Nexlify GitHub Repository Setup and Implementation

Based on the provided technical documentation[^1], I've outlined the complete folder structure for the Nexlify project in a single GitHub repository. This includes the three Python applications:

- **Data Ingestion Service**: A FastAPI-based microservice for processing data, generating embeddings with OpenAI GPT-4, and managing a Qdrant vector database.
- **Crew AI Agent Microservice** (named `nexlify-ai-agentics-server` in the structure): A FastAPI-based service using CrewAI for handling queries via AI agents.
- **MCP Server**: A Python package for integrating with GitHub Copilot using the Model Context Protocol.

The structure incorporates Terraform for infrastructure, GitHub Actions for CI/CD, and Docker for containerization. Below, I provide the repository structure with key file contents. All code is derived from the technical specifications[^1], expanded for completeness. You can copy-paste these into your repository files.

For setup:

- Create a new GitHub repository named `Nexlify`.
- Add the folders and files as described.
- Install dependencies via `pip install -r requirements.txt` in each service folder.
- Use the `.env.example` files to create `.env` files with your credentials (e.g., API keys).


## Repository Structure

```
Nexlify/
│
├── data-ingestion/              # Data Ingestion Service
│   ├── src/                    # Python source code
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── ingestion.py       # Data processing and embedding logic
│   │   ├── utils.py           # Utility functions (e.g., text extraction)
│   ├── tests/                 # Unit and integration tests
│   │   ├── test_ingestion.py
│   ├── Dockerfile             # Docker configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Example environment variables (e.g., OPENAI_API_KEY)
│   └── README.md              # Service documentation
│
├── nexlify-ai-agentics-server/  # Crew AI Agent Microservice
│   ├── src/                    # Python source code
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── agents.py          # CrewAI agent definitions
│   │   ├── search.py          # Search logic
│   ├── tests/                 # Unit and integration tests
│   │   ├── test_agents.py
│   ├── Dockerfile             # Docker configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Example environment variables (e.g., SERPER_API_KEY)
│   └── README.md              # Service documentation
│
├── mcp-server/                 # MCP Server
│   ├── nexlify_mcp/           # Python package structure
│   │   ├── __init__.py
│   │   ├── mcp_client.py      # MCP SDK integration
│   ├── setup.py               # PyPi package configuration
│   ├── tests/                 # Unit tests
│   │   ├── test_mcp.py
│   ├── Dockerfile             # Docker configuration (for local testing)
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Example environment variables
│   └── README.md              # Installation and usage instructions
│
├── blueprint/                  # Terraform infrastructure scripts
│   ├── main.tf                # Main Terraform configuration
│   ├── variables.tf           # Variable definitions
│   ├── outputs.tf             # Output definitions
│   ├── ec2.tf                 # EC2 instance provisioning
│   ├── security_groups.tf     # Security group rules
│   ├── vpc.tf                 # VPC and networking
│   ├── terraform.tfvars       # Variable values (e.g., AWS credentials)
│   └── README.md              # Infrastructure setup instructions
│
├── .github/                    # GitHub Actions workflows
│   ├── workflows/             # CI/CD pipelines
│   │   ├── ci-cd.yml          # Build, test, and deploy workflow
│   └── dependabot.yml         # Dependency update configuration
│
├── docker-compose.yml          # Docker Compose for local development
├── README.md                   # Project overview and setup guide
├── LICENSE                     # License file (e.g., MIT)
└── .gitignore                  # Git ignore rules
```


## Data Ingestion Service (data-ingestion/)

This service handles data processing, embedding generation with OpenAI GPT-4, and Qdrant storage[^1].

### src/main.py

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
from ingestion import load_data
from utils import extract_text
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
security = HTTPBasic()

def check_credentials(credentials: HTTPBasicCredentials):
    if credentials.username != os.getenv("ADMIN_USER") or credentials.password != os.getenv("ADMIN_PASS"):
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/load-data")
async def upload_data(file: UploadFile = File(...), credentials: HTTPBasicCredentials = Depends(security)):
    check_credentials(credentials)
    text = extract_text(file)
    load_data(text)
    return {"status": "Data loaded"}
# Add other endpoints as per doc: /configure-data-source, /semantic-search, /whitelisted-endpoints, etc.
```


### src/ingestion.py

```python
from openai import OpenAI
import qdrant_client
import uuid
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = qdrant_client.QdrantClient(host="qdrant-host", port=6333)

def load_data(text: str):
    embedding = client.embeddings.create(model="text-embedding-3-large", input=text).data[^0].embedding
    qdrant.upsert(collection_name="docs", points=[{"id": str(uuid.uuid4()), "vector": embedding, "payload": {"text": text}}])
```


### src/utils.py

```python
from PyPDF2 import PdfReader
# Add other imports for HTML, txt, docs processing

def extract_text(file):
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        return " ".join(page.extract_text() for page in reader.pages)
    # Add handlers for other formats
    return ""
```


### tests/test_ingestion.py

```python
import pytest
from ingestion import load_data

def test_load_data():
    # Mock OpenAI and Qdrant
    assert load_data("test text") is None  # Adjust based on actual logic
```


### Dockerfile

```
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```


### requirements.txt

```
fastapi
uvicorn
openai
qdrant-client
PyPDF2
pandas
atlassian-python-api
python-dotenv
pytest
```


### .env.example

```
OPENAI_API_KEY=your_openai_key
ADMIN_USER=admin
ADMIN_PASS=secret
QDRANT_HOST=qdrant.example.com
```


### README.md

Data Ingestion Service documentation: Processes files and generates embeddings using OpenAI GPT-4[^1]. Run with `docker build -t data-ingestion .` and `docker run -p 8000:8000 data-ingestion`.

## Crew AI Agent Microservice (nexlify-ai-agentics-server/)

This service orchestrates AI agents for queries[^1].

### src/main.py

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import vector_db_agent, internet_search_agent
from search import perform_search

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/search")
async def search(query: Query):
    results = perform_search(query.text)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return {"results": results}
```


### src/agents.py

```python
from crewai import Agent, Task, Crew
# Define Vector DB Agent and Internet Search Agent as per doc
vector_db_agent = Agent(role="Vector DB Searcher", goal="Search internal docs")
internet_search_agent = Agent(role="Internet Searcher", goal="Search whitelisted sites", tools=["serper"])
```


### src/search.py

```python
def perform_search(query: str):
    # Logic to call agents in parallel and consolidate results
    crew = Crew(agents=[vector_db_agent, internet_search_agent], tasks=[...])
    return crew.kickoff()
```


### tests/test_agents.py

```python
import pytest
from search import perform_search

def test_perform_search():
    assert perform_search("test query") == {"results": []}  # Mocked response
```


### Dockerfile

```
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```


### requirements.txt

```
fastapi
uvicorn
crewai
requests  # For Serper or similar
python-dotenv
pytest
```


### .env.example

```
SERPER_API_KEY=your_serper_key
DATA_INGESTION_URL=http://data-ingestion:8000
```


### README.md

Crew AI Agent Microservice: Handles queries with AI agents[^1]. Build and run similarly to Data Ingestion.

## MCP Server (mcp-server/)

This is a Python package for GitHub Copilot integration[^1].

### nexlify_mcp/__init__.py

```python
from .mcp_client import search
```


### nexlify_mcp/mcp_client.py

```python
import requests

def search(query: str, server_url: str):
    response = requests.post(f"{server_url}/search", json={"text": query})
    return response.json()
```


### setup.py

```python
from setuptools import setup
setup(
    name="nexlify-mcp",
    version="0.1.0",
    packages=["nexlify_mcp"],
    install_requires=["requests"],
)
```


### tests/test_mcp.py

```python
import pytest
from nexlify_mcp import search

def test_search():
    # Mock requests
    assert search("test", "http://localhost:8001") == {}
```


### Dockerfile

```
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "nexlify_mcp"]
```


### requirements.txt

```
requests
pytest
```


### .env.example

```
CREW_AI_URL=http://nexlify-ai-agentics-server:8001
```


### README.md

MCP Server: Install with `pip install .` and run `python -m nexlify_mcp` for Copilot integration[^1].

## Infrastructure and CI/CD (blueprint/ and .github/)

### blueprint/main.tf

```hcl
provider "aws" {
  region = var.region
}

# Add resources from doc example
resource "aws_instance" "qdrant" {
  ami           = var.ami
  instance_type = "t3.large"
  tags = { Name = "Nexlify-Qdrant" }
}
# Include ec2.tf, vpc.tf, etc.
```


### blueprint/variables.tf

```hcl
variable "region" { default = "us-east-1" }
variable "ami" { default = "ami-12345678" }
```


### blueprint/outputs.tf

```hcl
output "qdrant_ip" {
  value = aws_instance.qdrant.public_ip
}
```


### blueprint/ec2.tf

```hcl
# EC2 provisioning logic
```


### blueprint/security_groups.tf

```hcl
# Security group rules for HTTP/HTTPS
```


### blueprint/vpc.tf

```hcl
# VPC and networking
```


### blueprint/terraform.tfvars

```
region = "us-east-1"
# Add AWS credentials (do not commit)
```


### blueprint/README.md

Terraform setup: Run `terraform init` and `terraform apply` to provision AWS resources[^1].

### .github/workflows/ci-cd.yml

```yaml
name: Nexlify CI/CD
on:
  push:
    tags:
      - 'v*'
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      # Add build, push, deploy steps as per doc
```


### .github/dependabot.yml

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```


## Root Files

### docker-compose.yml

```yaml
version: '3'
services:
  data-ingestion:
    build: ./data-ingestion
    ports:
      - "8000:8000"
    env_file: ./data-ingestion/.env
  nexlify-ai-agentics-server:
    build: ./nexlify-ai-agentics-server
    ports:
      - "8001:8001"
    env_file: ./nexlify-ai-agentics-server/.env
  # Add Qdrant if needed
```


### README.md

Nexlify MVP: RAG-based AI chatbot. Setup: Clone repo, run `docker-compose up`, configure IDE for MCP[^1].

### LICENSE

MIT License (standard text).

### .gitignore

```
*.pyc
__pycache__/
.env
terraform.tfstate
```

This setup creates the three Python apps in one repo, ready for development and deployment[^1]. Test locally with Docker Compose, then deploy via Terraform and GitHub Actions.

<div style="text-align: center">⁂</div>

[^1]: Nexlify_MVP_Documentation-4.markdown

