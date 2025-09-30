import pytest
from mcp.rag_service import RAGService
from core.utils import Document

def test_rag_service_instantiation():
    rag_service = RAGService()
    assert rag_service is not None

def test_rag_service_e2e():
    rag_service = RAGService()
    docs = [
        Document(id="doc1", content="This is a test document about cats.", source="test"),
        Document(id="doc2", content="This is another test document about dogs.", source="test")
    ]
    rag_service.ingest(docs)
    answer = rag_service.ask("What are the documents about?")
    assert "cats" in answer.lower()
    assert "dogs" in answer.lower()
