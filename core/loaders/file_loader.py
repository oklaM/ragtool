"""This module provides a FileLoader class for loading documents from files."""

import os
from core.loader_base import LoaderBase
from core.utils import Document
import logging

logger = logging.getLogger(__name__)

class FileLoader(LoaderBase):
    """A class for loading documents from files."""
    def load(self, sources: list[str]) -> list[Document]:
        """Loads documents from a list of file paths."""
        logger.info(f"Loading files from {len(sources)} sources.")
        docs = []
        for source in sources:
            if os.path.isfile(source):
                try:
                    with open(source, 'r', encoding='utf-8') as f:
                        content = f.read()
                    docs.append(Document(id=source, source=source, content=content))
                    logger.info(f"Loaded file: {source}")
                except Exception as e:
                    logger.error(f"Error loading file {source}: {e}")
                    continue
            else:
                logger.warning(f"Source is not a file: {source}")
        logger.info(f"Loaded {len(docs)} documents.")
        return docs