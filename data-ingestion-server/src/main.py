from fastapi import FastAPI
from .api.ingest_view import router as ingest_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="NEXLIFY Ingestion API",
    description="NEXLIFY Ingestion API for Confluence and other data sources",
    version="1.0.0",
)

# CORS setup for mobile + web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ingest_router, prefix="/ingest")





@app.get("/")
async def root():
    return {"message": "Welcome to Nexlify"}
