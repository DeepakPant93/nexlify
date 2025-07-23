#!/usr/bin/env python
import sys
import warnings
import os

from nexlify_ai_agentics_server.crew import NexlifyAiAgenticsServer

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs'
    }
    NexlifyAiAgenticsServer().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        NexlifyAiAgenticsServer().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        NexlifyAiAgenticsServer().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        NexlifyAiAgenticsServer().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def app():
    """
    Run the FastAPI app.
    """
    from nexlify_ai_agentics_server.app import app as fastapi_app
    import uvicorn

    # Load environment variables
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = os.getenv("SERVER_PORT", "8000")
    log_level = os.getenv("LOG_LEVEL", "info")

    uvicorn.run(fastapi_app, host=host, port=int(port), log_level=log_level)
