
"""This module provides an Embedder class for generating vector embeddings."""

import abc
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import time

import logging

logger = logging.getLogger(__name__)

class Embedder(abc.ABC):
    """An abstract base class for embedders."""
    def __init__(self, model_name):
        """Initializes the Embedder."""
        self.model_name = model_name

    @abc.abstractmethod
    def embed(self, texts):
        """Generates embeddings for a list of texts."""
        pass

    def embed_query(self, query):
        """Generates an embedding for a single query."""
        return self.embed([query])[0]

class OpenAIEmbedder(Embedder):
    """An embedder that uses OpenAI's API."""
    def __init__(self, model_name, api_key):
        """Initializes the OpenAIEmbedder."""
        super().__init__(model_name)
        self.client = OpenAI(api_key=api_key)

    def embed(self, texts, batch_size=16):
        """Generates embeddings for a list of texts using OpenAI's API."""
        logger.info(f"Embedding {len(texts)} texts with OpenAI model {self.model_name}.")
        embs = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            resp = self.client.embeddings.create(input=batch_texts, model=self.model_name)
            for d in resp.data:
                embs.append(d.embedding)
            time.sleep(0.2)
        return embs

class SentenceTransformerEmbedder(Embedder):
    """An embedder that uses the sentence-transformers library."""
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initializes the SentenceTransformerEmbedder."""
        super().__init__(model_name)
        self._st_model = SentenceTransformer(model_name)

    def embed(self, texts):
        """Generates embeddings for a list of texts using sentence-transformers."""
        logger.info(f"Embedding {len(texts)} texts with SentenceTransformer model {self.model_name}.")
        embs = self._st_model.encode(texts, show_progress_bar=False)
        return [e.tolist() if hasattr(e, 'tolist') else e for e in embs]