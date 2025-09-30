"""This module provides a Faiss IVFPQ indexer."""

import faiss
import numpy as np
import json
from core.indexer import Indexer
from core.utils import Document
import logging

logger = logging.getLogger(__name__)

class IndexerFaissIVFPQ(Indexer):
    """A Faiss IVFPQ indexer."""
    def __init__(self, index_path='rag_index.faiss', nlist=128, m=8, nbits=8):
        """Initializes the IndexerFaissIVFPQ."""
        self.index_path = index_path
        self.nlist = nlist
        self.m = m
        self.nbits = nbits
        self._index = None
        self.chunks = []

    def index(self, chunks: list[Document], embeddings: list[list[float]]):
        """Indexes a list of chunks and their embeddings using Faiss IVFPQ."""
        logger.info(f"Indexing {len(chunks)} chunks.")
        self.chunks = chunks
        vectors = np.array(embeddings).astype('float32')
        dim = vectors.shape[1]

        if len(vectors) < 1000:
            logger.info("Using IndexFlatL2 for small dataset.")
            self._index = faiss.IndexFlatL2(dim)
        else:
            if len(vectors) < self.nlist:
                self.nlist = len(vectors)
            quantizer = faiss.IndexFlatL2(dim)
            logger.info(f"Using IndexIVFPQ with nlist={self.nlist}.")
            self._index = faiss.IndexIVFPQ(quantizer, dim, self.nlist, self.m, self.nbits)
            logger.info("Training index...")
            self._index.train(vectors)

        logger.info("Adding vectors to index.")
        self._index.add(vectors)
        
        logger.info(f"Writing index to {self.index_path}")
        faiss.write_index(self._index, self.index_path)
        with open(self.index_path + '.meta.json', 'w', encoding='utf-8') as f:
            json.dump([chunk.__dict__ for chunk in chunks], f, ensure_ascii=False)

    def search(self, query_embedding: list[float], top_k: int) -> list[tuple[int, float]]:
        """Searches the index for the top_k most similar chunks."""
        logger.info(f"Searching for top {top_k} results.")
        if not self._index:
            logger.info(f"Loading index from {self.index_path}")
            self._index = faiss.read_index(self.index_path)
            with open(self.index_path + '.meta.json', 'r', encoding='utf-8') as f:
                self.chunks = [Document(**chunk) for chunk in json.load(f)]

        distances, indices = self._index.search(np.array([query_embedding]).astype('float32'), top_k)
        
        results = []
        for i in range(top_k):
            if i < len(indices[0]):
                chunk_index = indices[0][i]
                score = distances[0][i]
                results.append((self.chunks[chunk_index], score))
        logger.info(f"Found {len(results)} results.")
        return results
