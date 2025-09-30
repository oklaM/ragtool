"""FastAPI application for the RAG Toolkit."""

from fastapi import FastAPI
from pydantic import BaseModel
from mcp.rag_service import RAGService
from core.loaders.file_loader import FileLoader
from core.loaders.url_loader import UrlLoader

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='RAG Toolkit API')

rag_service = RAGService()
file_loader = FileLoader()
url_loader = UrlLoader()

class IngestRequest(BaseModel):
    """Request model for the /ingest endpoint."""
    sources: list[str]

class AskRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str

@app.post("/ingest")
def ingest(request: IngestRequest):
    """Ingests documents from a list of sources."""
    logger.info(f"Ingesting sources: {request.sources}")
    docs = []
    # Simple way to distinguish between url and file path
    urls = [source for source in request.sources if source.startswith('http')]
    files = [source for source in request.sources if not source.startswith('http')]

    if urls:
        logger.info(f"Loading URLs: {urls}")
        docs.extend(url_loader.load(urls))
    if files:
        logger.info(f"Loading files: {files}")
        docs.extend(file_loader.load(files))

    rag_service.ingest(docs)
    logger.info(f"Ingested {len(docs)} documents.")
    return {"status": "ok"}

@app.post("/ask")
def ask(request: AskRequest):
    """Asks a question to the RAG toolkit."""
    logger.info(f"Received question: {request.question}")
    answer = rag_service.ask(request.question)
    logger.info(f"Returning answer: {answer}")
    return {"answer": answer}

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
