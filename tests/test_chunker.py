import pytest
from core.chunker import Chunker
from core.utils import Document

def test_chunker_instantiation():
    chunker = Chunker()
    assert chunker is not None

def test_chunker_simple_text():
    chunker = Chunker(chunk_size=10, chunk_overlap=2)
    doc = Document(id="test_doc", content="This is a test document.", source="test")
    chunks = chunker.chunk(doc)
    assert len(chunks) > 0
    assert chunks[0].content == "This is a "

def test_chunker_empty_document():
    chunker = Chunker()
    doc = Document(id="empty_doc", content="", source="test")
    chunks = chunker.chunk(doc)
    assert len(chunks) == 0

def test_chunker_no_sentence_endings():
    chunker = Chunker(chunk_size=10)
    doc = Document(id="no_sentence_end", content="This is a long sentence with no ending", source="test")
    chunks = chunker.chunk(doc)
    assert len(chunks) == 1
    assert chunks[0].content == "This is a long sentence with no ending"

def test_chunker_smaller_than_chunk_size():
    chunker = Chunker(chunk_size=100)
    doc = Document(id="small_doc", content="This is a small document.", source="test")
    chunks = chunker.chunk(doc)
    assert len(chunks) == 1
    assert chunks[0].content == "This is a small document."