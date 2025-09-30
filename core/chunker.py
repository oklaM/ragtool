"""This module provides a Chunker class for splitting documents into smaller chunks."""

import re
from core.utils import Document
import logging

logger = logging.getLogger(__name__)

class Chunker:
    """A class for splitting documents into smaller chunks."""
    def __init__(self, chunk_size=2000, chunk_overlap=200):
        """Initializes the Chunker."""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.sentence_end = re.compile(r'(?<=[.!?])\s+')

    def chunk(self, doc: Document) -> list[Document]:
        """Chunks a document into a list of smaller documents."""
        logger.info(f"Chunking document: {doc.id}")
        if not doc.content:
            logger.warning(f"Document {doc.id} has no content.")
            return []
        
        sentences = self._split_into_sentences(doc.content)
        
        chunks_content = self._chunk_sentences(sentences)

        chunks = []
        for i, content in enumerate(chunks_content):
            chunks.append(Document(
                id=f"{doc.id}#chunk-{i}",
                source=doc.source,
                content=content,
                metadata=doc.metadata
            ))
        logger.info(f"Generated {len(chunks)} chunks for document {doc.id}.")
        return chunks

    def _split_into_sentences(self, text: str) -> list[str]:
        """Splits a text into a list of sentences."""
        if not text:
            return []
        parts = self.sentence_end.split(text.strip())
        return [p.strip() for p in parts if p.strip()]

    def _chunk_sentences(self, sentences: list[str]) -> list[str]:
        """Chunks a list of sentences into a list of strings."""
        chunks = []
        cur = []
        cur_len = 0
        for s in sentences:
            if cur_len + len(s) + 1 <= self.chunk_size:
                cur.append(s)
                cur_len += len(s) + 1
            else:
                if cur:
                    chunks.append(' '.join(cur))
                
                if len(s) > self.chunk_size:
                    start = 0
                    while start < len(s):
                        chunks.append(s[start:start+self.chunk_size])
                        start += self.chunk_size - self.chunk_overlap
                    cur = []
                    cur_len = 0
                else:
                    cur = [s]
                    cur_len = len(s)
        if cur:
            chunks.append(' '.join(cur))
        
        if self.chunk_overlap and len(chunks) > 1:
            out = []
            for i, c in enumerate(chunks):
                if i == 0:
                    out.append(c)
                else:
                    prev = out[-1]
                    tail = prev[-self.chunk_overlap:] if len(prev) > self.chunk_overlap else prev
                    out.append(tail + '\n' + c)
            return out

        return chunks