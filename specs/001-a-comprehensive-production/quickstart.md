# Quickstart for RAG Toolkit

This guide provides a basic example of how to use the RAG toolkit to answer questions from a set of documents.

## 1. Initialize the Toolkit

First, initialize the `RAGToolkit` with a vector store (e.g., Faiss) and a list of data sources.

```python
from rag_toolkit import RAGToolkit

# Initialize the toolkit with a Faiss vector store
toolkit = RAGToolkit(vector_store='faiss')
```

## 2. Ingest Documents

Next, ingest documents from your data sources. The toolkit will automatically process and index them.

```python
# Ingest documents from a list of URLs and local text files
toolkit.ingest(data_sources=['http://example.com/article1', 'path/to/document.txt'])
```

## 3. Ask a Question

Once the documents are ingested, you can ask questions.

```python
# Ask a question
answer = toolkit.ask(question="What is the main topic of the documents?")

print(answer)
```
