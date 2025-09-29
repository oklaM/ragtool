import faiss, numpy as np, json
from core import constants

def load_index(index_path=None):
    if not index_path:
        raise ValueError("index_path must be provided")
    
    index = faiss.read_index(index_path)
    with open(index_path + '.meta.json', 'r', encoding='utf-8') as f:
        meta = json.load(f)
    return index, meta

def retrieve_top_k(query_emb, top_k=5, index_path=None):
    index, meta = load_index(index_path)
    D, I = index.search(np.array([query_emb]).astype('float32'), top_k)
    hits = []
    for dist, idx in zip(D[0], I[0]):
        if idx < 0: continue
        item = meta[idx]
        hits.append({'score': float(dist), 'meta': item})
    return hits
