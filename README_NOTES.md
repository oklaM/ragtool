Production Notes:

- OCR (pytesseract) requires system tesseract. On Debian/Ubuntu: `sudo apt-get install -y tesseract-ocr`.
- For MinIO local S3 testing: docker-compose includes a MinIO service. Use MINIO credentials from .env or defaults in compose.
- Secrets: store OPENAI_API_KEY, NOTION_TOKEN, MCP_API_KEY, and AWS credentials in a secret manager or env; do NOT commit.
- Milvus: tune index params (nlist, metric) for your data size. The provided Milvus in compose is for testing.
- Tests: add integration tests for Chroma/Milvus with local containers in CI if needed.
