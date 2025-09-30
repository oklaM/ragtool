# RAG Tool — Production-ready Retrieval-Augmented Generation System

A comprehensive, production-ready RAG (Retrieval-Augmented Generation) toolkit that enables intelligent document retrieval and question-answering capabilities. Built with modularity and scalability in mind, supporting multiple data sources and vector databases.

## 🚀 Features

### Core Capabilities
- **Multi-source Data Ingestion**: URL, files, PDFs, Notion databases, S3 storage
- **Intelligent Text Chunking**: Sentence-aware chunking with configurable overlap
- **Flexible Embedding Models**: OpenAI embeddings or local Sentence Transformers
- **Multiple Vector Databases**: FAISS (default), ChromaDB, and Milvus support
- **RESTful API**: FastAPI-based MCP (Model Context Protocol) service
- **Production-ready**: Authentication, health checks, error handling

### Data Source Support
- **URL Loading**: Web page content extraction
- **File Processing**: Markdown, text files with glob patterns
- **PDF Documents**: Text extraction with OCR support via pytesseract
- **Notion Integration**: Direct database connection
- **S3 Storage**: Cloud storage integration
- **OCR Capabilities**: Image text recognition

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Tesseract OCR (for image processing)

### Installation

1. **Clone and setup environment**:
```bash
git clone <repository-url>
cd rag_tool_final
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Start the API server**:
```bash
uvicorn mcp.api:app --host 0.0.0.0 --port 8000
```

### Basic Usage

1. **Ingest documents**:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"sources": ["path/to/your/file.txt"]}' http://localhost:8000/ingest
```

2. **Ask a question**:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"question": "What is in the document?"}' http://localhost:8000/ask
```

## 🏗️ Architecture

### Core Components

#### 1. Data Loaders (`core/loaders/`)
- **FileLoader**: Local file system access
- **URLLoader**: Web content extraction
- **PDFLoader**: PDF text extraction with OCR
- **NotionLoader**: Notion database integration
- **S3Loader**: AWS S3 storage access

#### 2. Processing Pipeline
- **Chunker**: Intelligent text segmentation
- **Embedder**: Vector embedding generation
- **Indexer**: Vector database management

#### 3. Storage Backends
- **FAISS**: Fast local similarity search
- **ChromaDB**: Persistent vector database
- **Milvus**: Scalable vector database

#### 4. API Layer
- **FastAPI Server**: RESTful endpoints
- **MCP Protocol**: Standardized model communication
- **Authentication**: API key security

## ⚙️ Configuration

### Main Configuration (`configs/config.yaml`)

```yaml
sources:
  - type: url
    value: https://example.com/docs
  - type: file
    value: ./data/*.md

embedding:
  provider: auto  # openai | sentence-transformers
  model: text-embedding-3-small

index:
  type: faiss  # faiss | chroma | milvus
  path: rag_index.faiss

pipeline:
  chunk_max_chars: 2000
  chunk_overlap: 200
```

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for embeddings
- `NOTION_TOKEN`: Notion integration token
- `MCP_API_KEY`: API authentication key
- `AWS_*`: AWS credentials for S3 access

## 🔧 Advanced Usage

### Custom Data Sources
Extend the system by creating new loader classes:

```python
from core.loader_base import LoaderBase

class CustomLoader(LoaderBase):
    def load(self):
        # Your implementation
        return documents
```

### Multiple Index Backends

**FAISS (Default)**:
```yaml
index:
  type: faiss
  path: ./my_index.faiss
```

**ChromaDB**:
```yaml
index:
  type: chroma
  persist_directory: ./chroma_db
```

**Milvus**:
```yaml
index:
  type: milvus
  collection_name: rag_docs
```

### API Integration

```python
import requests

# Ingest documents
requests.post("http://localhost:8000/ingest", json={"sources": ["path/to/your/file.txt"]})

# Ask a question
response = requests.post("http://localhost:8000/ask", json={"question": "What is in the document?"})
print(response.json()["answer"])
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 🚀 Deployment

### Production Deployment
For production deployment, consider the following approaches:

1. **Traditional Server Deployment**:
   - Deploy on cloud servers (AWS EC2, GCP Compute Engine, etc.)
   - Use process managers like systemd or supervisor
   - Set up reverse proxy with nginx

2. **Containerized Deployment**:
   - Create a Dockerfile for containerization
   - Use orchestration tools like Kubernetes
   - Implement proper health checks and monitoring

### Production Considerations
- Use environment variables for secrets
- Configure proper logging and monitoring
- Set up health check endpoints
- Implement rate limiting if needed
- Use HTTPS in production

## 📊 Performance

- **Embedding**: Batch processing with configurable sizes
- **Indexing**: Optimized for large document collections
- **Querying**: Sub-second response times for typical queries
- **Scalability**: Supports distributed vector databases

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions:
- Check the `README_NOTES.md` for deployment tips
- Review the example configurations
- Examine the test cases for usage patterns

---

**Built with ❤️ for production RAG applications**
