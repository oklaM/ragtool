"""This module provides an abstract base class for indexers."""

import abc

class Indexer(abc.ABC):
    """An abstract base class for indexers."""
    @abc.abstractmethod
    def index(self, chunks, embeddings):
        """Indexes a list of chunks and their embeddings."""
        pass

    @abc.abstractmethod
    def search(self, query_embedding, top_k):
        """Searches the index for the top_k most similar chunks."""
        pass