import pytest
from core.embedder import SentenceTransformerEmbedder
from core.utils import Document

def test_embedder_instantiation():
    embedder = SentenceTransformerEmbedder()
    assert embedder is not None

def test_embedder_simple_text():
    embedder = SentenceTransformerEmbedder()
    doc = Document(id="test_doc", content="This is a test document.", source="test")
    embeddings = embedder.embed([doc.content])
    assert len(embeddings) == 1
    assert len(embeddings[0]) > 0