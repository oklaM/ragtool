import re

SENTENCE_END = re.compile(r'(?<=[.!?])\s+')

def split_into_sentences(text):
    if not text:
        return []
    parts = SENTENCE_END.split(text.strip())
    return [p.strip() for p in parts if p.strip()]

def chunk_text(text, max_chars=2000, overlap=200):
    sentences = split_into_sentences(text)
    chunks = []
    cur = []
    cur_len = 0
    for s in sentences:
        if cur_len + len(s) + 1 <= max_chars:
            cur.append(s)
            cur_len += len(s) + 1
        else:
            if cur:
                chunks.append(' '.join(cur))
            if len(s) > max_chars:
                start = 0
                while start < len(s):
                    chunks.append(s[start:start+max_chars])
                    start += max_chars - overlap
                cur = []
                cur_len = 0
            else:
                cur = [s]
                cur_len = len(s) + 1
    if cur:
        chunks.append(' '.join(cur))
    if overlap and len(chunks) > 1:
        out = []
        for i, c in enumerate(chunks):
            if i == 0:
                out.append(c)
            else:
                prev = out[-1]
                tail = prev[-overlap:] if len(prev) > overlap else prev
                out.append(tail + '\n' + c)
        return out
    return chunks

def docs_to_chunks(docs, max_chars=2000, overlap=200):
    out = []
    for doc in docs:
        chunks = chunk_text(doc['text'], max_chars, overlap)
        for i, c in enumerate(chunks):
            out.append({
                'id': f"{doc['id']}#chunk-{i}",
                'source': doc.get('meta', {}).get('source', doc['id']),
                'title': doc.get('meta', {}).get('title'),
                'text': c,
                'meta': doc.get('meta', {})
            })
    return out
