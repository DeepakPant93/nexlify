FROM python:3.12-slim

# Update system packages to address vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Install UV package manager
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN pip install --upgrade pip && pip install uv crewai

# Set working directory
WORKDIR /app

# Copy requirements and application files
COPY pyproject.toml .

# Build dependencies using UV
RUN crewai install

COPY . .

# Expose port for FastAPI
EXPOSE 8000

ENV SERVER_PORT="8000"
ENV SERVER_HOST="0.0.0.0"
ENV MODEL=gemini/gemini-1.5-flash

# Define build argument for API key
ARG MODEL_API_KEY
ENV MODEL_API_KEY=${MODEL_API_KEY}

# Run the FastAPI application
CMD ["uv", "run", "app"]
