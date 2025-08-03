from fastapi import FastAPI
from pydantic import BaseModel
from nexlify_ai_agentics_server.crew import NexlifyAiAgenticsServer

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    response: str

ERROR_MESSAGE = "Please check the inputs and try again. If the issue persists, contact support."

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):

    try:
        output = NexlifyAiAgenticsServer().crew().kickoff(inputs={"query": request.query})
    except Exception:
        output = None

    response = ERROR_MESSAGE if output is None else output.raw
    return SearchResponse(response=response)
