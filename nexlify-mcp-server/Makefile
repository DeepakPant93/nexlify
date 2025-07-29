.PHONY: help run build install publish

PYTHON_PATH ?= /usr/local/bin/python3.12  # Default Python path; override as needed
PYPI_TOKEN ?=  # PyPI publish token; override when running make (e.g., make publish PYPI_TOKEN=your-token)

help: ## Display available commands
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Application commands

run: ## Run the application
	uv run app

build: ## Build the application
	uv build

install: ## Install the local build package (For Development only) 
	uv pip install --python $(PYTHON_PATH) dist/nexlify_mcp_server-0.1.1-py3-none-any.whl

publish: build ## Publish the application
	uv publish --token $(PYPI_TOKEN)
