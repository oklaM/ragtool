def chunk_text(text, max_chars=2000, overlap=200):
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(L, start + max_chars)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
        if start >= L:
            break
    return chunks

def docs_to_chunks(docs, max_chars=2000, overlap=200):
    out = []
    for doc in docs:
        chunks = chunk_text(doc['text'], max_chars, overlap)
        for i, c in enumerate(chunks):
            out.append({
                'id': f"{doc['id']}#chunk-{i}",
                'source': doc.get('meta',{}).get('source', doc['id']),
                'title': doc.get('meta',{}).get('title'),
                'text': c,
                'meta': doc.get('meta',{})
            })
    return out
