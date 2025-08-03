# Nexlify AI Agentics Server Crew

Welcome to the NexlifyAiAgenticsServer Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.12 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv: 

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Customizing

**Add your environment variables into the `.env` file, taking reference from the `.env.example` file:**

- `MODEL=gemini/gemini-1.5-flash`
- `MODEL_API_KEY=<model_api_key>` # Your API key here. Generate a new API key for the GEMINI model from the [AI Studio](https://aistudio.google.com/app/apikey) website.
- `NEXLIFY_DATA_INGESTION_SERVICE_BASE_URI`=http://localhost:7860 # Base URI for the Nexlify Data Ingestion Service
- `SERPER_API_KEY`=<serper_api_key> # Generate your Serper API key from the [Serper API](https://serper.dev/api-keys) website.

- Modify `src/nexlify_ai_agentics_server/config/agents.yaml` to define your agents
- Modify `src/nexlify_ai_agentics_server/config/tasks.yaml` to define your tasks
- Modify `src/nexlify_ai_agentics_server/crew.py` to add your own logic, tools, and specific args
- Modify `src/nexlify_ai_agentics_server/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, use the following make commands from the root folder of your project:

```bash
make run
```

This command initializes the nexlify-ai-agentics-server Crew, assembling the agents and assigning them tasks as defined in your configuration. The Swagger documentation will be available at [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs).

### Additional Make Commands

- `make build`                          Build the application
- `make bake-container`                 Build Docker container
- `make run-container MODEL_API_KEY=your_key`  Run Docker container
- `make container-push`                 Push container to registry
- `make bake-container-and-push`        Build and push container
- `make bake`                           Setup development environment

## Deployment

To deploy the application, ensure you have added the required environment variables to the `.env` file as described in the Customizing section. Then, use the following command to run the app locally:

```bash
make run
```

For containerized deployment, use the `make bake-container` and `make run-container MODEL_API_KEY=your_key` commands to build and run the Docker container.

## DockerHub

The official Docker image for the Nexlify AI Agentics Server is available on DockerHub:

📦 **[deepak93p/nexlify-ai-agentics-server](https://hub.docker.com/r/deepak93p/nexlify-ai-agentics-server)**

## Understanding Your Crew

The nexlify-ai-agentics-server Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For additional help or inquiries, please refer to the [crewAI documentation](https://crewai.com) or reach out to the community for support.

## License

This project is released under the [MIT License](../LICENSE).