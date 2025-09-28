from core.chunker import chunk_text

def test_chunk_small():
    s = 'a'*500
    chunks = chunk_text(s, max_chars=200, overlap=50)
    assert len(chunks) >= 3
