import os, time, numpy as np
from core.utils import load_config
try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None
CONF = load_config()
EMBED_MODEL = os.getenv('EMBED_MODEL', CONF.get('EMBED_MODEL'))
USE_OPENAI = bool(CONF.get('OPENAI_API_KEY')) and EMBED_MODEL and EMBED_MODEL.startswith('text-embedding')
if not USE_OPENAI:
    if SentenceTransformer is None:
        raise RuntimeError('sentence-transformers not available; install or set OPENAI_API_KEY')
    _st_model = SentenceTransformer('all-MiniLM-L6-v2')
else:
    import openai
    openai.api_key = CONF.get('OPENAI_API_KEY')

def embed_texts_local(texts):
    embs = _st_model.encode(texts, show_progress_bar=False)
    return [e.tolist() if hasattr(e, 'tolist') else e for e in embs]

def embed_texts_openai(texts, model='text-embedding-3-small', batch=16):
    import openai
    embs = []
    for i in range(0, len(texts), batch):
        batch_texts = texts[i:i+batch]
        resp = openai.Embedding.create(input=batch_texts, model=model)
        for d in resp.data:
            embs.append(d.embedding)
        time.sleep(0.2)
    return embs

def embed_chunks(chunks):
    texts = [c['text'] for c in chunks]
    if USE_OPENAI:
        vecs = embed_texts_openai(texts, model=EMBED_MODEL or 'text-embedding-3-small')
    else:
        vecs = embed_texts_local(texts)
    for c, v in zip(chunks, vecs):
        c['embedding'] = v
    return chunks
