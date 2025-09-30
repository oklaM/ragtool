"""This module provides a UrlLoader class for loading documents from URLs."""

import requests
from bs4 import BeautifulSoup
from core.loader_base import LoaderBase
from core.utils import Document
import logging

logger = logging.getLogger(__name__)

class UrlLoader(LoaderBase):
    """A class for loading documents from URLs."""
    def load(self, sources: list[str]) -> list[Document]:
        """Loads documents from a list of URLs."""
        logger.info(f"Loading URLs from {len(sources)} sources.")
        docs = []
        for url in sources:
            try:
                response = requests.get(url, headers={"User-Agent": "rag-tool-bot/1.0"}, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text from the body, trying to get meaningful content
                if soup.body:
                    text = soup.body.get_text(separator='\n', strip=True)
                else:
                    text = soup.get_text(separator='\n', strip=True)

                docs.append(Document(id=url, source=url, content=text))
                logger.info(f"Loaded URL: {url}")
            except Exception as e:
                logger.error(f"Error loading URL {url}: {e}")
                continue
        logger.info(f"Loaded {len(docs)} documents.")
        return docs