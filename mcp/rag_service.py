"""This module provides a high-level RAG service."""

from core.chunker import Chunker
from core.embedder import SentenceTransformerEmbedder
from core.indexer_faiss_ivfpq import IndexerFaissIVFPQ
from core.retriever import Retriever
from core.utils import Document
import logging

logger = logging.getLogger(__name__)

class RAGService:
    """A high-level service for Retrieval-Augmented Generation."""
    def __init__(self, index_path='rag_index.faiss'):
        """Initializes the RAGService."""
        self.chunker = Chunker()
        self.embedder = SentenceTransformerEmbedder()
        self.indexer = IndexerFaissIVFPQ(index_path)
        self.retriever = Retriever(self.indexer, self.embedder)

    def ingest(self, docs: list[Document]):
        """Ingests a list of documents into the RAG system."""
        logger.info(f"Ingesting {len(docs)} documents.")
        chunks = []
        for doc in docs:
            logger.info(f"Chunking document: {doc.id}")
            chunks.extend(self.chunker.chunk(doc))
        
        logger.info(f"Generated {len(chunks)} chunks.")
        chunk_contents = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed(chunk_contents)

        logger.info("Indexing chunks.")
        self.indexer.index(chunks, embeddings)
        logger.info("Indexing complete.")

    def ask(self, query: str, top_k=5) -> str:
        """Asks a question to the RAG system."""
        logger.info(f"Retrieving top {top_k} results for query: {query}")
        results = self.retriever.retrieve(query, top_k=top_k)
        logger.info(f"Retrieved {len(results)} results.")
        
        # For now, just concatenate the content of the retrieved chunks
        # In a real application, this would be fed to a language model
        return " ".join([result.content for result in results])