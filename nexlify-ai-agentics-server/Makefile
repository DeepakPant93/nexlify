# Variables
DOCKERHUB_USERNAME ?= deepak93p
IMAGE_NAME ?= $(DOCKERHUB_USERNAME)/nexlify-ai-agentics-server
TAG ?= latest
MODEL_API_KEY ?=

.PHONY: run build bake-container container-push bake-container-and-push help setup-dev

help: ## Display available commands
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Application commands
run: ## Run the application
	uv run app

build: ## Build the application
	uv build

# Docker commands
bake-container: ## Build Docker container
	docker build -t $(IMAGE_NAME):$(TAG) -f Dockerfile .

run-container: ## Run Docker container (Usage: make run-container MODEL_API_KEY=your_key)
ifndef MODEL_API_KEY
	$(error MODEL_API_KEY is not set. Please set MODEL_API_KEY environment variable)
endif
	docker run -p 8000:8000 -e MODEL_API_KEY=$(MODEL_API_KEY) $(IMAGE_NAME):$(TAG)

container-push: ## Push container to registry
	docker push $(IMAGE_NAME):$(TAG)

bake-container-and-push: bake-container container-push ## Build and push container

bake: ## Setup development environment
	pip install --upgrade pip && pip install uv crewai

