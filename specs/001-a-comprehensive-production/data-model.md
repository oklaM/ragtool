# Data Model for RAG Toolkit

## Document

*   **Description**: Represents a single piece of content ingested into the system.
*   **Attributes**:
    *   `source`: The origin of the document (e.g., URL, file path).
    *   `content`: The text content of the document.
    *   `metadata`: A dictionary of additional information about the document.

## DataSource

*   **Description**: Represents a source of documents.
*   **Examples**: A file folder, a database, a Notion workspace.

## VectorStore

*   **Description**: Represents the vector database used for storing document embeddings.
*   **Examples**: Faiss, Chroma, Milvus.

## Query

*   **Description**: Represents a user's question in natural language.

## Answer

*   **Description**: Represents the system's response to a query.
