"""This module provides utility classes and functions for the RAG toolkit."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Document:
    """A class representing a document."""
    id: str
    source: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)