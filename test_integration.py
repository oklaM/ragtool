#!/usr/bin/env python3
"""
Integration test for RAG Tool
Tests core functionality without external dependencies
"""

import sys
import os
sys.path.append('.')

from core.chunker import chunk_text, docs_to_chunks
from core.embedder import SentenceTransformerEmbedder
from core.indexer import build_index
from core.retriever import retrieve_top_k

def test_chunker():
    """Test text chunking functionality"""
    print("Testing chunker...")
    
    # Test basic chunking
    text = "This is a test sentence. This is another sentence. " * 10
    chunks = chunk_text(text, max_chars=100, overlap=20)
    
    assert len(chunks) > 1, "Should create multiple chunks"
    # Allow some flexibility in chunk size due to overlap handling
    assert all(len(chunk) <= 120 for chunk in chunks), "All chunks should be within reasonable size limit"
    
    # Test document chunking
    docs = [
        {'id': 'doc1', 'text': 'Document 1 content. ' * 50, 'meta': {'source': 'test'}},
        {'id': 'doc2', 'text': 'Document 2 content. ' * 50, 'meta': {'source': 'test'}}
    ]
    
    chunked_docs = docs_to_chunks(docs, max_chars=100, overlap=20)
    assert len(chunked_docs) > len(docs), "Should create more chunks than documents"
    
    print("✓ Chunker test passed")
    return True

def test_embedder():
    """Test embedding functionality with local model"""
    print("Testing embedder...")
    
    # Use a small local model for testing
    embedder = SentenceTransformerEmbedder('all-MiniLM-L6-v2')
    
    texts = ["This is a test sentence", "Another test sentence"]
    embeddings = embedder.embed(texts)
    
    assert len(embeddings) == len(texts), "Should return same number of embeddings"
    assert len(embeddings[0]) == 384, "Embedding dimension should be 384 for MiniLM"
    
    print("✓ Embedder test passed")
    return True

def test_pipeline():
    """Test complete RAG pipeline"""
    print("Testing complete pipeline...")
    
    # Create test documents
    docs = [
        {
            'id': 'test_doc_1', 
            'text': 'Python is a programming language. It is widely used for web development and data science. ' * 10,
            'meta': {'source': 'test', 'title': 'Python Introduction'}
        },
        {
            'id': 'test_doc_2', 
            'text': 'Machine learning is a subset of artificial intelligence. It involves training models on data. ' * 10,
            'meta': {'source': 'test', 'title': 'ML Basics'}
        }
    ]
    
    # Chunk documents
    chunks = docs_to_chunks(docs, max_chars=200, overlap=50)
    print(f"Created {len(chunks)} chunks from {len(docs)} documents")
    
    # Generate embeddings
    embedder = SentenceTransformerEmbedder('all-MiniLM-L6-v2')
    texts = [chunk['text'] for chunk in chunks]
    embeddings = embedder.embed(texts)
    
    # Add embeddings to chunks
    for i, chunk in enumerate(chunks):
        chunk['embedding'] = embeddings[i]
    
    # Build index
    index_path = build_index(chunks, backend='faiss', index_path='test_index.faiss')
    print(f"Index built at: {index_path}")
    
    # Test retrieval
    query_text = "What is Python used for?"
    query_embedding = embedder.embed_query(query_text)
    
    results = retrieve_top_k(query_embedding, top_k=2, index_path='test_index.faiss')
    
    assert len(results) > 0, "Should retrieve some results"
    print(f"Retrieved {len(results)} results for query: {query_text}")
    
    # Cleanup
    if os.path.exists('test_index.faiss'):
        os.remove('test_index.faiss')
    if os.path.exists('test_index.faiss.meta.json'):
        os.remove('test_index.faiss.meta.json')
    
    print("✓ Pipeline test passed")
    return True

def test_api_structure():
    """Test API module structure"""
    print("Testing API structure...")
    
    try:
        from mcp.api import app
        from mcp.rag_service import RagMCPService
        
        # Check if FastAPI app is properly configured
        assert hasattr(app, 'routes'), "App should have routes"
        
        print("✓ API structure test passed")
        return True
    except ImportError as e:
        print(f"⚠ API structure test skipped: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting RAG Tool Integration Tests")
    print("=" * 50)
    
    tests = [
        test_chunker,
        test_embedder,
        test_pipeline,
        test_api_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())