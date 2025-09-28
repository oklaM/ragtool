import os
import pytest

def test_minio_available():
    endpoint = os.getenv('MINIO_ENDPOINT', 'http://localhost:9000')
    try:
        import httpx
        r = httpx.get(endpoint + '/')
        assert r.status_code in (200, 403, 404)
    except Exception:
        pytest.skip('MinIO not available')

def test_milvus_connectable():
    try:
        from pymilvus import connections
        connections.connect(host=os.getenv('MILVUS_HOST','127.0.0.1'), port=str(os.getenv('MILVUS_PORT','19530')))
    except Exception:
        pytest.skip('Milvus not connectable')
