import pytest
from fastapi.testclient import TestClient
from mcp.api import app
import os

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ask_endpoint():
    # Create a dummy file and ingest it
    with open("test_ask.txt", "w") as f:
        f.write("The meaning of life is 42.")
    client.post("/ingest", json={"sources": ["test_ask.txt"]})
    os.remove("test_ask.txt")

    response = client.post("/ask", json={"question": "What is the meaning of life?"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "42" in response.json()["answer"]

def test_ingest_endpoint():
    # Create a dummy file
    with open("test_ingest.txt", "w") as f:
        f.write("This is a test.")
    
    response = client.post("/ingest", json={"sources": ["test_ingest.txt"]})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    os.remove("test_ingest.txt")