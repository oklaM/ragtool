"""This module provides an abstract base class for loaders."""

import abc
from core.utils import Document

class LoaderBase(abc.ABC):
    """An abstract base class for loaders."""
    @abc.abstractmethod
    def load(self, sources: list[str]) -> list[Document]:
        """Loads documents from a list of sources."""
        pass