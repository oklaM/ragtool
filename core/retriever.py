"""This module provides a Retriever class for retrieving documents from an index."""

from core.embedder import Embedder
from core.indexer import Indexer
from core.utils import Document
import logging

logger = logging.getLogger(__name__)

class Retriever:
    """A class for retrieving documents from an index."""
    def __init__(self, indexer: Indexer, embedder: Embedder):
        """Initializes the Retriever."""
        self.indexer = indexer
        self.embedder = embedder

    def retrieve(self, query: str, top_k: int = 5) -> list[Document]:
        """Retrieves the top_k most relevant documents for a given query."""
        logger.info(f"Retrieving top {top_k} documents for query: {query}")
        query_embedding = self.embedder.embed_query(query)
        search_results = self.indexer.search(query_embedding, top_k)
        
        # The search method of the indexer returns a list of (document, score) tuples.
        # We are only interested in the documents here.
        results = [result[0] for result in search_results]
        logger.info(f"Retrieved {len(results)} documents.")
        return results